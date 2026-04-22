from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import *

class PineScriptLexer(RegexLexer):
    name = 'PineScript'
    aliases = ['pinescript', 'pine']
    filenames = ['*.pine']
    
    KEYWORDS = [
        'if', 'else', 'for', 'while', 'switch', 'break', 'continue',
        'export', 'import', 'method', 'type', 'varip', 'var', 'const',
        'true', 'false', 'na', 'and', 'or', 'not', 'in', 'enum'
    ]
    
    BUILT_IN_VARIABLES = [
        'open', 'high', 'low', 'close', 'volume', 'time', 'hl2', 'hlc3',
        'ohlc4', 'hlcc4', 'bar_index', 'last_bar_index', 'barstate', 
        'syminfo', 'timeframe', 'timenow', 'dayofmonth', 'dayofweek',
        'hour', 'minute', 'month', 'second', 'year', 'weekofyear'
    ]
    
    BUILT_IN_FUNCTIONS = [
        # Declaration functions
        'indicator', 'strategy', 'library',
        
        # Plot functions
        'plot', 'plotshape', 'plotchar', 'plotcandle', 'plotbar', 'plotarrow',
        'hline', 'fill', 'bgcolor', 'barcolor',
        
        # Technical Analysis
        'ta.sma', 'ta.ema', 'ta.wma', 'ta.vwma', 'ta.swma', 'ta.alma',
        'ta.rsi', 'ta.macd', 'ta.stoch', 'ta.cci', 'ta.mfi', 'ta.roc',
        'ta.atr', 'ta.tr', 'ta.bb', 'ta.bbw', 'ta.kc', 'ta.kcw', 'ta.dmi',
        'ta.adx', 'ta.supertrend', 'ta.sar', 'ta.obv', 'ta.wad', 'ta.wvad',
        'ta.crossover', 'ta.crossunder', 'ta.cross', 'ta.valuewhen',
        'ta.highest', 'ta.lowest', 'ta.highestbars', 'ta.lowestbars',
        'ta.barssince', 'ta.change', 'ta.mom', 'ta.cum', 'ta.correlation',
        'ta.percentrank', 'ta.percentile_linear_interpolation',
        'ta.percentile_nearest_rank', 'ta.median', 'ta.mode', 'ta.range',
        'ta.stdev', 'ta.variance', 'ta.dev', 'ta.cog', 'ta.linreg',
        'ta.pivothigh', 'ta.pivotlow',
        
        # Math functions
        'math.abs', 'math.acos', 'math.asin', 'math.atan', 'math.avg',
        'math.ceil', 'math.cos', 'math.exp', 'math.floor', 'math.log',
        'math.log10', 'math.max', 'math.min', 'math.pow', 'math.random',
        'math.round', 'math.round_to_mintick', 'math.sign', 'math.sin',
        'math.sqrt', 'math.sum', 'math.tan', 'math.todegrees', 'math.toradians',
        
        # String functions
        'str.tostring', 'str.tonumber', 'str.format', 'str.length',
        'str.contains', 'str.pos', 'str.substring', 'str.lower', 'str.upper',
        'str.replace', 'str.replace_all', 'str.split', 'str.match',
        
        # Array functions
        'array.new', 'array.from', 'array.new_bool', 'array.new_int',
        'array.new_float', 'array.new_string', 'array.new_color',
        'array.new_line', 'array.new_label', 'array.new_box',
        'array.get', 'array.set', 'array.push', 'array.pop', 'array.shift',
        'array.unshift', 'array.insert', 'array.remove', 'array.clear',
        'array.size', 'array.slice', 'array.reverse', 'array.sort',
        'array.concat', 'array.copy', 'array.fill', 'array.includes',
        'array.indexof', 'array.lastindexof', 'array.join', 'array.first',
        'array.last', 'array.max', 'array.min', 'array.sum', 'array.avg',
        'array.median', 'array.mode', 'array.variance', 'array.stdev',
        'array.covariance', 'array.range', 'array.binary_search',
        
        # Matrix functions
        'matrix.new', 'matrix.get', 'matrix.set', 'matrix.rows', 'matrix.columns',
        'matrix.add', 'matrix.sub', 'matrix.mult', 'matrix.sum', 'matrix.avg',
        'matrix.max', 'matrix.min', 'matrix.transpose', 'matrix.det',
        'matrix.inv', 'matrix.pinv', 'matrix.rank', 'matrix.trace',
        
        # Map functions
        'map.new', 'map.get', 'map.put', 'map.remove', 'map.clear',
        'map.size', 'map.keys', 'map.values', 'map.contains',
        
        # Request functions
        'request.security', 'request.security_lower_tf', 'request.dividends',
        'request.splits', 'request.earnings', 'request.financial',
        'request.quandl', 'request.seed', 'request.economic',
        
        # Input functions
        'input', 'input.int', 'input.float', 'input.bool', 'input.string',
        'input.color', 'input.timeframe', 'input.symbol', 'input.source',
        'input.price', 'input.session', 'input.time', 'input.text_area',
        
        # Color functions
        'color.new', 'color.rgb', 'color.from_gradient', 'color.r', 'color.g',
        'color.b', 'color.t',
        
        # Line/Label/Box functions
        'line.new', 'line.delete', 'line.get_price', 'line.get_x1', 'line.get_x2',
        'line.get_y1', 'line.get_y2', 'line.set_color', 'line.set_extend',
        'line.set_style', 'line.set_width', 'line.set_x1', 'line.set_x2',
        'line.set_xy1', 'line.set_xy2', 'line.set_y1', 'line.set_y2',
        'label.new', 'label.delete', 'label.get_text', 'label.get_x', 'label.get_y',
        'label.set_color', 'label.set_size', 'label.set_style', 'label.set_text',
        'label.set_textcolor', 'label.set_tooltip', 'label.set_x', 'label.set_xy',
        'label.set_y', 'label.set_yloc',
        'box.new', 'box.delete', 'box.get_bottom', 'box.get_left', 'box.get_right',
        'box.get_top', 'box.set_bgcolor', 'box.set_border_color', 'box.set_border_style',
        'box.set_border_width', 'box.set_bottom', 'box.set_extend', 'box.set_left',
        'box.set_lefttop', 'box.set_right', 'box.set_rightbottom', 'box.set_top',
        
        # Table functions
        'table.new', 'table.cell', 'table.clear', 'table.delete',
        'table.set_bgcolor', 'table.set_border_color', 'table.set_border_width',
        'table.set_frame_color', 'table.set_frame_width',
        
        # Strategy functions
        'strategy.entry', 'strategy.order', 'strategy.exit', 'strategy.close',
        'strategy.close_all', 'strategy.cancel', 'strategy.cancel_all',
        'strategy.risk.allow_entry_in', 'strategy.risk.max_cons_loss_days',
        'strategy.risk.max_drawdown', 'strategy.risk.max_intraday_filled_orders',
        'strategy.risk.max_intraday_loss', 'strategy.risk.max_position_size',
        
        # Alert functions
        'alert', 'alertcondition',
        
        # Other functions
        'bool', 'int', 'float', 'string', 'color', 'timestamp', 'nz', 'na',
        'fixnan', 'sign', 'abs', 'min', 'max', 'avg', 'sum', 'log', 'log.info',
        'log.warning', 'log.error', 'runtime.log', 'runtime.error'
    ]
    
    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'//.*?$', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
            (words(BUILT_IN_VARIABLES, suffix=r'\b'), Name.Builtin),
            (words(BUILT_IN_FUNCTIONS, suffix=r'\b'), Name.Function),
            (r'@version\s*=\s*\d+', Comment.Preproc),
            (r'"([^"\\]|\\.)*"', String.Double),
            (r"'([^'\\]|\\.)*'", String.Single),
            (r'\b\d+\.?\d*([eE][+-]?\d+)?\b', Number.Float),
            (r'\b\d+\b', Number.Integer),
            (r'[+\-*/%]', Operator),
            (r'[=!<>]=?', Operator),
            (r'=>', Operator),
            (r'[(){}\[\],.:?]', Punctuation),
            (r'[a-zA-Z_]\w*', Name),
        ],
        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
    }
