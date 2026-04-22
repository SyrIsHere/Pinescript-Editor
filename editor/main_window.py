from PyQt6.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, 
                             QVBoxLayout, QWidget, QMenuBar, QStatusBar, QTabWidget, QMenu)
from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtGui import QAction, QKeySequence
from .editor_widget import EditorWidget
from .theme_manager import ThemeManager
from .snippets import SnippetManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.theme_manager.load_theme("dark")
        self.snippet_manager = SnippetManager()
        
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        self.setWindowTitle("Pine Script Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        self.new_file()
        self.create_menu_bar()
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(lambda: self.current_editor().undo())
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(lambda: self.current_editor().redo())
        edit_menu.addAction(redo_action)
        
        view_menu = menubar.addMenu("&View")
        
        dark_theme_action = QAction("Dark Theme", self)
        dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        view_menu.addAction(dark_theme_action)
        
        light_theme_action = QAction("Light Theme", self)
        light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        view_menu.addAction(light_theme_action)
        
        insert_menu = menubar.addMenu("&Insert")
        snippets_menu = insert_menu.addMenu("&Snippets")
        for key, snippet in self.snippet_manager.get_all_snippets().items():
            action = QAction(snippet['name'], self)
            action.setStatusTip(snippet['description'])
            action.triggered.connect(lambda checked, k=key: self.insert_snippet(k))
            snippets_menu.addAction(action)
        
        help_menu = menubar.addMenu("&Help")
        
        docs_action = QAction("Pine Script Documentation", self)
        docs_action.triggered.connect(self.open_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def new_file(self):
        editor = EditorWidget(self.theme_manager)
        index = self.tab_widget.addTab(editor, "Untitled")
        self.tab_widget.setCurrentIndex(index)
        editor.textChanged.connect(lambda: self.mark_modified(self.tab_widget.currentIndex()))
        
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Pine Script Files (*.pine);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                editor = EditorWidget(self.theme_manager)
                editor.setPlainText(content)
                
                file_info = QFileInfo(filename)
                index = self.tab_widget.addTab(editor, file_info.fileName())
                self.tab_widget.setCurrentIndex(index)
                self.tab_widget.setTabToolTip(index, filename)
                
                editor.textChanged.connect(lambda: self.mark_modified(self.tab_widget.currentIndex()))
                self.status_bar.showMessage(f"Opened: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
    
    def save_file(self):
        current_tab = self.tab_widget.currentIndex()
        filename = self.tab_widget.tabToolTip(current_tab)
        
        if not filename:
            self.save_file_as()
        else:
            self._save_to_file(filename)
    
    def save_file_as(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Pine Script Files (*.pine);;All Files (*)"
        )
        
        if filename:
            self._save_to_file(filename)
    
    def _save_to_file(self, filename):
        try:
            editor = self.current_editor()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            
            current_tab = self.tab_widget.currentIndex()
            file_info = QFileInfo(filename)
            self.tab_widget.setTabText(current_tab, file_info.fileName())
            self.tab_widget.setTabToolTip(current_tab, filename)
            
            self.status_bar.showMessage(f"Saved: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.current_editor().clear()
    
    def current_editor(self):
        return self.tab_widget.currentWidget()
    
    def mark_modified(self, index):
        current_text = self.tab_widget.tabText(index)
        if not current_text.endswith("*"):
            self.tab_widget.setTabText(index, current_text + "*")
    
    def change_theme(self, theme_name):
        self.theme_manager.load_theme(theme_name)
        self.apply_theme()
        
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if isinstance(editor, EditorWidget):
                editor.highlighter.update_formats()
                editor.highlighter.rehighlight()
                editor.highlight_current_line()
        
        self.status_bar.showMessage(f"Theme changed to: {theme_name}")
    
    def insert_snippet(self, snippet_key):
        snippet = self.snippet_manager.get_snippet(snippet_key)
        if snippet:
            editor = self.current_editor()
            if editor:
                cursor = editor.textCursor()
                cursor.insertText(snippet['code'])
                self.status_bar.showMessage(f"Inserted: {snippet['name']}")
    
    def open_documentation(self):
        import webbrowser
        webbrowser.open("https://www.tradingview.com/pine-script-docs/")
    
    def show_about(self):
        QMessageBox.about(self, "About Pine Script Editor",
                         "<h2>Pine Script Editor</h2>"
                         "<p>Professional editor for Pine Script V6</p>"
                         "<p>Features:</p>"
                         "<ul>"
                         "<li>Complete syntax highlighting</li>"
                         "<li>Intelligent autocomplete (Ctrl+Space)</li>"
                         "<li>Real-time syntax validation</li>"
                         "<li>Built-in snippets</li>"
                         "<li>Auto-indent and bracket matching</li>"
                         "<li>Customizable themes</li>"
                         "</ul>"
                         "<p>Version 1.0</p>")
    
    def apply_theme(self):
        self.theme_manager.apply_theme(self)
        colors = self.theme_manager.current_theme['colors']
        
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background: {colors['editor_background']};
            }}
            QTabBar::tab {{
                background: {colors['tab_inactive']};
                color: {colors['foreground']};
                padding: 8px 16px;
                border: 1px solid {colors['border']};
            }}
            QTabBar::tab:selected {{
                background: {colors['tab_active']};
            }}
            QTabBar::tab:hover {{
                background: {colors['tab_hover']};
            }}
        """)
