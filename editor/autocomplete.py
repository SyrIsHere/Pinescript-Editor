from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont

class AutoCompleteWidget(QListWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        font = QFont("Consolas", 10)
        self.setFont(font)
        
        self.itemClicked.connect(self.insert_completion)
        self.hide()
        
    def show_completions(self, completions, cursor_rect):
        if not completions:
            self.hide()
            return
            
        self.clear()
        for completion in completions:
            item = QListWidgetItem(completion['text'])
            item.setData(Qt.ItemDataRole.UserRole, completion)
            self.addItem(item)
        
        pos = self.editor.mapToGlobal(cursor_rect.bottomLeft())
        self.move(pos)
        self.setFixedWidth(300)
        self.setFixedHeight(min(200, len(completions) * 25))
        self.setCurrentRow(0)
        self.show()
        
    def insert_completion(self, item):
        completion = item.data(Qt.ItemDataRole.UserRole)
        cursor = self.editor.textCursor()
        
        cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor, len(self.current_word))
        cursor.removeSelectedText()
        
        cursor.insertText(completion['insert'])
        self.editor.setTextCursor(cursor)
        self.hide()
        
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Tab):
            if self.currentItem():
                self.insert_completion(self.currentItem())
        elif event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            super().keyPressEvent(event)
        else:
            self.hide()
            self.editor.keyPressEvent(event)

class AutoCompleteProvider:
    def __init__(self):
        self.keywords = self._load_keywords()
        self.functions = self._load_functions()
        self.variables = self._load_variables()
        
    def _load_keywords(self):
        return {
            'if': {'text': 'if', 'insert': 'if ', 'type': 'keyword', 'desc': 'Conditional statement'},
            'else': {'text': 'else', 'insert': 'else\n    ', 'type': 'keyword', 'desc': 'Else clause'},
            'for': {'text': 'for', 'insert': 'for ', 'type': 'keyword', 'desc': 'For loop'},
            'while': {'text': 'while', 'insert': 'while ', 'type': 'keyword', 'desc': 'While loop'},
            'switch': {'text': 'switch', 'insert': 'switch ', 'type': 'keyword', 'desc': 'Switch statement'},
            'var': {'text': 'var', 'insert': 'var ', 'type': 'keyword', 'desc': 'Variable declaration'},
            'varip': {'text': 'varip', 'insert': 'varip ', 'type': 'keyword', 'desc': 'Intrabar persist variable'},
            'const': {'text': 'const', 'insert': 'const ', 'type': 'keyword', 'desc': 'Constant declaration'},
            'export': {'text': 'export', 'insert': 'export ', 'type': 'keyword', 'desc': 'Export for library'},
            'import': {'text': 'import', 'insert': 'import ', 'type': 'keyword', 'desc': 'Import library'},
            'method': {'text': 'method', 'insert': 'method ', 'type': 'keyword', 'desc': 'Method definition'},
            'type': {'text': 'type', 'insert': 'type ', 'type': 'keyword', 'desc': 'User-defined type'},
            'true': {'text': 'true', 'insert': 'true', 'type': 'keyword', 'desc': 'Boolean true'},
            'false': {'text': 'false', 'insert': 'false', 'type': 'keyword', 'desc': 'Boolean false'},
            'na': {'text': 'na', 'insert': 'na', 'type': 'keyword', 'desc': 'Not available value'},
        }
    
    def _load_functions(self):
        return {
            'indicator': {'text': 'indicator()', 'insert': 'indicator("", "", overlay=true)', 'type': 'function', 
                         'desc': 'Declares an indicator script'},
            'strategy': {'text': 'strategy()', 'insert': 'strategy("", "", overlay=true)', 'type': 'function',
                        'desc': 'Declares a strategy script'},
            'library': {'text': 'library()', 'insert': 'library("")', 'type': 'function',
                       'desc': 'Declares a library script'},
            
            'plot': {'text': 'plot()', 'insert': 'plot(, "", )', 'type': 'function',
                    'desc': 'Plots a series of data'},
            'plotshape': {'text': 'plotshape()', 'insert': 'plotshape(, "", , , )', 'type': 'function',
                         'desc': 'Plots visual shapes'},
            'plotchar': {'text': 'plotchar()', 'insert': 'plotchar(, "", , , )', 'type': 'function',
                        'desc': 'Plots a character'},
            'plotcandle': {'text': 'plotcandle()', 'insert': 'plotcandle(, , , , "", )', 'type': 'function',
                          'desc': 'Plots candlestick chart'},
            'plotbar': {'text': 'plotbar()', 'insert': 'plotbar(, , , , "", )', 'type': 'function',
                       'desc': 'Plots OHLC bars'},
            'hline': {'text': 'hline()', 'insert': 'hline(, "", )', 'type': 'function',
                     'desc': 'Horizontal line'},
            'fill': {'text': 'fill()', 'insert': 'fill(, , )', 'type': 'function',
                    'desc': 'Fills between two plots'},
            'bgcolor': {'text': 'bgcolor()', 'insert': 'bgcolor()', 'type': 'function',
                       'desc': 'Colors the background'},
            'barcolor': {'text': 'barcolor()', 'insert': 'barcolor()', 'type': 'function',
                        'desc': 'Colors the bars'},
            
            'ta.sma': {'text': 'ta.sma()', 'insert': 'ta.sma(close, 14)', 'type': 'function',
                      'desc': 'Simple Moving Average'},
            'ta.ema': {'text': 'ta.ema()', 'insert': 'ta.ema(close, 14)', 'type': 'function',
                      'desc': 'Exponential Moving Average'},
            'ta.wma': {'text': 'ta.wma()', 'insert': 'ta.wma(close, 14)', 'type': 'function',
                      'desc': 'Weighted Moving Average'},
            'ta.vwma': {'text': 'ta.vwma()', 'insert': 'ta.vwma(close, 14)', 'type': 'function',
                       'desc': 'Volume Weighted Moving Average'},
            'ta.rsi': {'text': 'ta.rsi()', 'insert': 'ta.rsi(close, 14)', 'type': 'function',
                      'desc': 'Relative Strength Index'},
            'ta.macd': {'text': 'ta.macd()', 'insert': 'ta.macd(close, 12, 26, 9)', 'type': 'function',
                       'desc': 'MACD indicator'},
            'ta.stoch': {'text': 'ta.stoch()', 'insert': 'ta.stoch(close, high, low, 14)', 'type': 'function',
                        'desc': 'Stochastic oscillator'},
            'ta.cci': {'text': 'ta.cci()', 'insert': 'ta.cci(close, 20)', 'type': 'function',
                      'desc': 'Commodity Channel Index'},
            'ta.atr': {'text': 'ta.atr()', 'insert': 'ta.atr(14)', 'type': 'function',
                      'desc': 'Average True Range'},
            'ta.tr': {'text': 'ta.tr', 'insert': 'ta.tr', 'type': 'variable',
                     'desc': 'True Range'},
            'ta.crossover': {'text': 'ta.crossover()', 'insert': 'ta.crossover(, )', 'type': 'function',
                            'desc': 'Checks if series1 crosses over series2'},
            'ta.crossunder': {'text': 'ta.crossunder()', 'insert': 'ta.crossunder(, )', 'type': 'function',
                             'desc': 'Checks if series1 crosses under series2'},
            'ta.cross': {'text': 'ta.cross()', 'insert': 'ta.cross(, )', 'type': 'function',
                        'desc': 'Checks if two series cross'},
            'ta.highest': {'text': 'ta.highest()', 'insert': 'ta.highest(high, 14)', 'type': 'function',
                          'desc': 'Highest value over period'},
            'ta.lowest': {'text': 'ta.lowest()', 'insert': 'ta.lowest(low, 14)', 'type': 'function',
                         'desc': 'Lowest value over period'},
            'ta.barssince': {'text': 'ta.barssince()', 'insert': 'ta.barssince()', 'type': 'function',
                            'desc': 'Bars since condition was true'},
            'ta.change': {'text': 'ta.change()', 'insert': 'ta.change(close)', 'type': 'function',
                         'desc': 'Difference between current and previous value'},
            'ta.mom': {'text': 'ta.mom()', 'insert': 'ta.mom(close, 10)', 'type': 'function',
                      'desc': 'Momentum'},
            'ta.roc': {'text': 'ta.roc()', 'insert': 'ta.roc(close, 10)', 'type': 'function',
                      'desc': 'Rate of Change'},
            
            'math.abs': {'text': 'math.abs()', 'insert': 'math.abs()', 'type': 'function',
                        'desc': 'Absolute value'},
            'math.max': {'text': 'math.max()', 'insert': 'math.max(, )', 'type': 'function',
                        'desc': 'Maximum of two values'},
            'math.min': {'text': 'math.min()', 'insert': 'math.min(, )', 'type': 'function',
                        'desc': 'Minimum of two values'},
            'math.round': {'text': 'math.round()', 'insert': 'math.round()', 'type': 'function',
                          'desc': 'Rounds to nearest integer'},
            'math.floor': {'text': 'math.floor()', 'insert': 'math.floor()', 'type': 'function',
                          'desc': 'Rounds down'},
            'math.ceil': {'text': 'math.ceil()', 'insert': 'math.ceil()', 'type': 'function',
                         'desc': 'Rounds up'},
            'math.pow': {'text': 'math.pow()', 'insert': 'math.pow(, )', 'type': 'function',
                        'desc': 'Power function'},
            'math.sqrt': {'text': 'math.sqrt()', 'insert': 'math.sqrt()', 'type': 'function',
                         'desc': 'Square root'},
            'math.log': {'text': 'math.log()', 'insert': 'math.log()', 'type': 'function',
                        'desc': 'Natural logarithm'},
            'math.log10': {'text': 'math.log10()', 'insert': 'math.log10()', 'type': 'function',
                          'desc': 'Base-10 logarithm'},
            'math.exp': {'text': 'math.exp()', 'insert': 'math.exp()', 'type': 'function',
                        'desc': 'Exponential function'},
            'math.sin': {'text': 'math.sin()', 'insert': 'math.sin()', 'type': 'function',
                        'desc': 'Sine function'},
            'math.cos': {'text': 'math.cos()', 'insert': 'math.cos()', 'type': 'function',
                        'desc': 'Cosine function'},
            'math.tan': {'text': 'math.tan()', 'insert': 'math.tan()', 'type': 'function',
                        'desc': 'Tangent function'},
            
            'str.tostring': {'text': 'str.tostring()', 'insert': 'str.tostring()', 'type': 'function',
                            'desc': 'Converts value to string'},
            'str.tonumber': {'text': 'str.tonumber()', 'insert': 'str.tonumber()', 'type': 'function',
                            'desc': 'Converts string to number'},
            'str.format': {'text': 'str.format()', 'insert': 'str.format("", )', 'type': 'function',
                          'desc': 'Formats string with placeholders'},
            'str.length': {'text': 'str.length()', 'insert': 'str.length()', 'type': 'function',
                          'desc': 'Returns string length'},
            'str.contains': {'text': 'str.contains()', 'insert': 'str.contains(, )', 'type': 'function',
                            'desc': 'Checks if string contains substring'},
            
            'array.new': {'text': 'array.new<type>()', 'insert': 'array.new<float>()', 'type': 'function',
                         'desc': 'Creates new array'},
            'array.from': {'text': 'array.from()', 'insert': 'array.from()', 'type': 'function',
                          'desc': 'Creates array from values'},
            'array.push': {'text': 'array.push()', 'insert': 'array.push(, )', 'type': 'function',
                          'desc': 'Adds element to end'},
            'array.pop': {'text': 'array.pop()', 'insert': 'array.pop()', 'type': 'function',
                         'desc': 'Removes and returns last element'},
            'array.get': {'text': 'array.get()', 'insert': 'array.get(, )', 'type': 'function',
                         'desc': 'Gets element at index'},
            'array.set': {'text': 'array.set()', 'insert': 'array.set(, , )', 'type': 'function',
                         'desc': 'Sets element at index'},
            'array.size': {'text': 'array.size()', 'insert': 'array.size()', 'type': 'function',
                          'desc': 'Returns array size'},
            'array.clear': {'text': 'array.clear()', 'insert': 'array.clear()', 'type': 'function',
                           'desc': 'Removes all elements'},
            
            'request.security': {'text': 'request.security()', 'insert': 'request.security(, , )', 'type': 'function',
                                'desc': 'Requests data from another symbol/timeframe'},
            
            'input.int': {'text': 'input.int()', 'insert': 'input.int(14, "")', 'type': 'function',
                         'desc': 'Integer input'},
            'input.float': {'text': 'input.float()', 'insert': 'input.float(1.0, "")', 'type': 'function',
                           'desc': 'Float input'},
            'input.bool': {'text': 'input.bool()', 'insert': 'input.bool(true, "")', 'type': 'function',
                          'desc': 'Boolean input'},
            'input.string': {'text': 'input.string()', 'insert': 'input.string("", "")', 'type': 'function',
                            'desc': 'String input'},
            'input.color': {'text': 'input.color()', 'insert': 'input.color(color.blue, "")', 'type': 'function',
                           'desc': 'Color input'},
            'input.timeframe': {'text': 'input.timeframe()', 'insert': 'input.timeframe("", "")', 'type': 'function',
                               'desc': 'Timeframe input'},
            'input.symbol': {'text': 'input.symbol()', 'insert': 'input.symbol("", "")', 'type': 'function',
                            'desc': 'Symbol input'},
        }
    
    def _load_variables(self):
        return {
            'open': {'text': 'open', 'insert': 'open', 'type': 'variable', 'desc': 'Open price of current bar'},
            'high': {'text': 'high', 'insert': 'high', 'type': 'variable', 'desc': 'High price of current bar'},
            'low': {'text': 'low', 'insert': 'low', 'type': 'variable', 'desc': 'Low price of current bar'},
            'close': {'text': 'close', 'insert': 'close', 'type': 'variable', 'desc': 'Close price of current bar'},
            'volume': {'text': 'volume', 'insert': 'volume', 'type': 'variable', 'desc': 'Volume of current bar'},
            'hl2': {'text': 'hl2', 'insert': 'hl2', 'type': 'variable', 'desc': '(high + low) / 2'},
            'hlc3': {'text': 'hlc3', 'insert': 'hlc3', 'type': 'variable', 'desc': '(high + low + close) / 3'},
            'ohlc4': {'text': 'ohlc4', 'insert': 'ohlc4', 'type': 'variable', 'desc': '(open + high + low + close) / 4'},
            'hlcc4': {'text': 'hlcc4', 'insert': 'hlcc4', 'type': 'variable', 'desc': '(high + low + close + close) / 4'},
            
            'bar_index': {'text': 'bar_index', 'insert': 'bar_index', 'type': 'variable', 'desc': 'Current bar index'},
            'time': {'text': 'time', 'insert': 'time', 'type': 'variable', 'desc': 'Current bar time'},
            
            'barstate.isfirst': {'text': 'barstate.isfirst', 'insert': 'barstate.isfirst', 'type': 'variable',
                                'desc': 'True on first bar'},
            'barstate.islast': {'text': 'barstate.islast', 'insert': 'barstate.islast', 'type': 'variable',
                               'desc': 'True on last bar'},
            'barstate.ishistory': {'text': 'barstate.ishistory', 'insert': 'barstate.ishistory', 'type': 'variable',
                                  'desc': 'True on historical bars'},
            'barstate.isrealtime': {'text': 'barstate.isrealtime', 'insert': 'barstate.isrealtime', 'type': 'variable',
                                   'desc': 'True on realtime bars'},
            'barstate.isnew': {'text': 'barstate.isnew', 'insert': 'barstate.isnew', 'type': 'variable',
                              'desc': 'True on first update of bar'},
            'barstate.isconfirmed': {'text': 'barstate.isconfirmed', 'insert': 'barstate.isconfirmed', 'type': 'variable',
                                    'desc': 'True when bar is closed'},
            
            'timeframe.period': {'text': 'timeframe.period', 'insert': 'timeframe.period', 'type': 'variable',
                                'desc': 'Current timeframe period'},
            'timeframe.multiplier': {'text': 'timeframe.multiplier', 'insert': 'timeframe.multiplier', 'type': 'variable',
                                    'desc': 'Current timeframe multiplier'},
            'timeframe.isdaily': {'text': 'timeframe.isdaily', 'insert': 'timeframe.isdaily', 'type': 'variable',
                                 'desc': 'True if daily timeframe'},
            'timeframe.isweekly': {'text': 'timeframe.isweekly', 'insert': 'timeframe.isweekly', 'type': 'variable',
                                  'desc': 'True if weekly timeframe'},
            'timeframe.ismonthly': {'text': 'timeframe.ismonthly', 'insert': 'timeframe.ismonthly', 'type': 'variable',
                                   'desc': 'True if monthly timeframe'},
            
            'syminfo.ticker': {'text': 'syminfo.ticker', 'insert': 'syminfo.ticker', 'type': 'variable',
                              'desc': 'Symbol ticker'},
            'syminfo.currency': {'text': 'syminfo.currency', 'insert': 'syminfo.currency', 'type': 'variable',
                                'desc': 'Symbol currency'},
            'syminfo.type': {'text': 'syminfo.type', 'insert': 'syminfo.type', 'type': 'variable',
                            'desc': 'Symbol type'},
        }
    
    def get_completions(self, word):
        if not word:
            return []
        
        word_lower = word.lower()
        completions = []
        
        for source in [self.keywords, self.functions, self.variables]:
            for key, value in source.items():
                if key.lower().startswith(word_lower):
                    completions.append(value)
        
        return sorted(completions, key=lambda x: x['text'])
