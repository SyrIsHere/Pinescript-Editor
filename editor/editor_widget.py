from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QToolTip
from PyQt6.QtCore import Qt, QRect, QSize, QTimer
from PyQt6.QtGui import QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from pygments import lex
from pygments.token import Token
from .pinescript_lexer import PineScriptLexer
from .autocomplete import AutoCompleteWidget, AutoCompleteProvider
from .syntax_validator import SyntaxValidator

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class PineScriptHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme_manager):
        super().__init__(document)
        self.lexer = PineScriptLexer()
        self.theme_manager = theme_manager
        self.update_formats()
        
    def update_formats(self):
        syntax_colors = self.theme_manager.get_syntax_colors()
        
        self.formats = {
            Token.Keyword: self._create_format(syntax_colors.get('keyword', '#569CD6')),
            Token.Name.Builtin: self._create_format(syntax_colors.get('builtin', '#4EC9B0')),
            Token.Name.Function: self._create_format(syntax_colors.get('function', '#DCDCAA')),
            Token.Comment: self._create_format(syntax_colors.get('comment', '#6A9955'), italic=True),
            Token.Comment.Single: self._create_format(syntax_colors.get('comment', '#6A9955'), italic=True),
            Token.Comment.Multiline: self._create_format(syntax_colors.get('comment', '#6A9955'), italic=True),
            Token.Comment.Preproc: self._create_format(syntax_colors.get('preprocessor', '#C586C0')),
            Token.String: self._create_format(syntax_colors.get('string', '#CE9178')),
            Token.String.Double: self._create_format(syntax_colors.get('string', '#CE9178')),
            Token.String.Single: self._create_format(syntax_colors.get('string', '#CE9178')),
            Token.Number: self._create_format(syntax_colors.get('number', '#B5CEA8')),
            Token.Number.Integer: self._create_format(syntax_colors.get('number', '#B5CEA8')),
            Token.Number.Float: self._create_format(syntax_colors.get('number', '#B5CEA8')),
            Token.Operator: self._create_format(syntax_colors.get('operator', '#D4D4D4')),
        }
    
    def _create_format(self, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    def highlightBlock(self, text):
        for token_type, value in lex(text, self.lexer):
            if token_type in self.formats:
                length = len(value)
                start = self.currentBlock().position() + text.index(value)
                self.setFormat(text.index(value), length, self.formats[token_type])

class EditorWidget(QPlainTextEdit):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        self.line_number_area = LineNumberArea(self)
        self.highlighter = PineScriptHighlighter(self.document(), theme_manager)
        
        self.autocomplete_widget = AutoCompleteWidget(self)
        self.autocomplete_provider = AutoCompleteProvider()
        self.autocomplete_timer = QTimer()
        self.autocomplete_timer.setSingleShot(True)
        self.autocomplete_timer.timeout.connect(self.show_autocomplete)
        
        self.validator = SyntaxValidator()
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate_syntax)
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.textChanged.connect(self.on_text_changed)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        
        self.setTabStopDistance(40)
        self.auto_indent_enabled = True
        self.bracket_matching_enabled = True
        
    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        
        colors = self.theme_manager.current_theme['colors']
        painter.fillRect(event.rect(), QColor(colors['line_number_background']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(colors['line_number_foreground']))
                painter.drawText(0, int(top), self.line_number_area.width() - 5, 
                               self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def highlight_current_line(self):
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            colors = self.theme_manager.current_theme['colors']
            line_color = QColor(colors['current_line'])
            
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def on_text_changed(self):
        self.autocomplete_timer.start(300)
        self.validation_timer.start(500)
    
    def show_autocomplete(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText()
        
        if len(word) >= 2:
            completions = self.autocomplete_provider.get_completions(word)
            if completions:
                cursor_rect = self.cursorRect()
                self.autocomplete_widget.current_word = word
                self.autocomplete_widget.show_completions(completions, cursor_rect)
    
    def validate_syntax(self):
        code = self.toPlainText()
        errors = self.validator.validate(code)
    
    def keyPressEvent(self, event):
        if self.autocomplete_widget.isVisible():
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Tab):
                if self.autocomplete_widget.currentItem():
                    self.autocomplete_widget.insert_completion(self.autocomplete_widget.currentItem())
                    return
            elif event.key() == Qt.Key.Key_Escape:
                self.autocomplete_widget.hide()
                return
            elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
                self.autocomplete_widget.keyPressEvent(event)
                return
        
        if event.key() == Qt.Key.Key_Space and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.show_autocomplete()
            return
        
        if event.key() == Qt.Key.Key_Backspace:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                block = cursor.block()
                text = block.text()
                pos = cursor.positionInBlock()
                
                if pos > 0 and text[:pos].strip() == '':
                    spaces_before = len(text[:pos])
                    
                    if spaces_before >= 4 and spaces_before % 4 == 0:
                        cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 4)
                        cursor.removeSelectedText()
                        return
        
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                
                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.beginEditBlock()
                
                while cursor.position() < end:
                    cursor.insertText('    ')
                    if not cursor.movePosition(QTextCursor.MoveOperation.NextBlock):
                        break
                    end += 4
                
                cursor.endEditBlock()
            else:
                cursor.insertText('    ')
            return
        
        if event.key() == Qt.Key.Key_Backtab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                
                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.beginEditBlock()
                
                while cursor.position() < end:
                    cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                    block = cursor.block()
                    text = block.text()
                    
                    spaces_to_remove = 0
                    for i, char in enumerate(text):
                        if char == ' ' and i < 4:
                            spaces_to_remove += 1
                        else:
                            break
                    
                    if spaces_to_remove > 0:
                        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, spaces_to_remove)
                        cursor.removeSelectedText()
                        end -= spaces_to_remove
                    
                    if not cursor.movePosition(QTextCursor.MoveOperation.NextBlock):
                        break
                
                cursor.endEditBlock()
            else:
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                block = cursor.block()
                text = block.text()
                
                spaces_to_remove = 0
                for i, char in enumerate(text):
                    if char == ' ' and i < 4:
                        spaces_to_remove += 1
                    else:
                        break
                
                if spaces_to_remove > 0:
                    cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, spaces_to_remove)
                    cursor.removeSelectedText()
            return
        
        if self.auto_indent_enabled and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            block = cursor.block()
            text = block.text()
            
            indent = 0
            for char in text:
                if char == ' ':
                    indent += 1
                elif char == '\t':
                    indent += 4
                else:
                    break
            
            text_stripped = text.strip()
            extra_indent = 0
            
            if text_stripped.startswith(('if ', 'if(', 'else', 'for ', 'for(', 'while ', 'while(', 
                                         'switch ', 'switch(', 'method ', 'type ')):
                extra_indent = 4
            elif text_stripped.endswith('=>'):
                extra_indent = 4
            
            super().keyPressEvent(event)
            
            cursor = self.textCursor()
            spaces = ' ' * (indent + extra_indent)
            cursor.insertText(spaces)
            self.setTextCursor(cursor)
            return
        
        if self.bracket_matching_enabled:
            brackets = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
            if event.text() in brackets:
                cursor = self.textCursor()
                cursor.insertText(event.text() + brackets[event.text()])
                cursor.movePosition(QTextCursor.MoveOperation.Left)
                self.setTextCursor(cursor)
                return
        
        super().keyPressEvent(event)
