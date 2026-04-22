class SnippetManager:
    def __init__(self):
        self.snippets = self._load_snippets()
    
    def _load_snippets(self):
        return {
            'indicator_basic': {
                'name': 'Basic Indicator',
                'description': 'Basic template for an indicator',
                'code': '''//@version=6
indicator("My Indicator", shorttitle="MI", overlay=true)

length = input.int(14, "Length", minval=1)

value = ta.sma(close, length)

plot(value, "Value", color.blue, 2)
'''
            },
            'strategy_basic': {
                'name': 'Basic Strategy',
                'description': 'Basic template for a strategy',
                'code': '''//@version=6
strategy("My Strategy", shorttitle="MS", overlay=true, 
         default_qty_type=strategy.percent_of_equity, default_qty_value=10)

fastLength = input.int(12, "Fast MA Length", minval=1)
slowLength = input.int(26, "Slow MA Length", minval=1)

fastMA = ta.ema(close, fastLength)
slowMA = ta.ema(close, slowLength)

longCondition = ta.crossover(fastMA, slowMA)
shortCondition = ta.crossunder(fastMA, slowMA)

if longCondition
    strategy.entry("Long", strategy.long)

if shortCondition
    strategy.entry("Short", strategy.short)

plot(fastMA, "Fast MA", color.blue)
plot(slowMA, "Slow MA", color.red)
'''
            },
            'ma_crossover': {
                'name': 'Moving Average Crossover',
                'description': 'Moving average crossover system',
                'code': '''
fastMA = ta.sma(close, 10)
slowMA = ta.sma(close, 20)

bullishCross = ta.crossover(fastMA, slowMA)
bearishCross = ta.crossunder(fastMA, slowMA)

plot(fastMA, "Fast MA", color.blue)
plot(slowMA, "Slow MA", color.red)
bgcolor(bullishCross ? color.new(color.green, 90) : bearishCross ? color.new(color.red, 90) : na)
'''
            },
            'rsi_strategy': {
                'name': 'RSI Strategy',
                'description': 'RSI-based strategy',
                'code': '''
rsiLength = input.int(14, "RSI Length")
rsiOverbought = input.int(70, "Overbought Level")
rsiOversold = input.int(30, "Oversold Level")

rsi = ta.rsi(close, rsiLength)

longCondition = ta.crossover(rsi, rsiOversold)
shortCondition = ta.crossunder(rsi, rsiOverbought)

plot(rsi, "RSI", color.purple)
hline(rsiOverbought, "Overbought", color.red)
hline(rsiOversold, "Oversold", color.green)
hline(50, "Middle", color.gray)
'''
            },
            'custom_function': {
                'name': 'Custom Function',
                'description': 'Custom function template',
                'code': '''
myFunction(source, length) =>
    sum = 0.0
    for i = 0 to length - 1
        sum := sum + source[i]
    sum / length

result = myFunction(close, 20)
plot(result, "My Function", color.blue)
'''
            },
            'custom_type': {
                'name': 'Custom Type (UDT)',
                'description': 'User-Defined Type',
                'code': '''type MyType
    float value1
    float value2
    string label

var myObject = MyType.new(0.0, 0.0, "")

myObject.value1 := close
myObject.value2 := high - low
myObject.label := "Bar " + str.tostring(bar_index)
'''
            },
            'array_usage': {
                'name': 'Array Usage',
                'description': 'Array usage example',
                'code': '''
var prices = array.new<float>()

array.push(prices, close)

if array.size(prices) > 50
    array.shift(prices)

avgPrice = array.avg(prices)
plot(avgPrice, "Average", color.orange)
'''
            },
            'alert_condition': {
                'name': 'Alert Condition',
                'description': 'Alert condition example',
                'code': '''
condition = ta.crossover(ta.rsi(close, 14), 70)

if condition
    alert("RSI crossed above 70!", alert.freq_once_per_bar)

plotshape(condition, "Alert", shape.triangleup, location.belowbar, color.yellow, size=size.small)
'''
            },
            'multi_timeframe': {
                'name': 'Multi-Timeframe Analysis',
                'description': 'Multi-timeframe analysis example',
                'code': '''
htfTimeframe = input.timeframe("1D", "Higher Timeframe")

htfClose = request.security(syminfo.tickerid, htfTimeframe, close)
htfMA = request.security(syminfo.tickerid, htfTimeframe, ta.sma(close, 20))

plot(htfClose, "HTF Close", color.blue, 2)
plot(htfMA, "HTF MA", color.red, 2)
'''
            },
            'table_display': {
                'name': 'Table Display',
                'description': 'Table display example',
                'code': '''
var table myTable = table.new(position.top_right, 2, 3, 
                               bgcolor=color.new(color.gray, 80),
                               border_width=1)

if barstate.islast
    table.cell(myTable, 0, 0, "Label", text_color=color.white)
    table.cell(myTable, 1, 0, "Value", text_color=color.white)
    
    table.cell(myTable, 0, 1, "Close")
    table.cell(myTable, 1, 1, str.tostring(close, "#.##"))
    
    table.cell(myTable, 0, 2, "Volume")
    table.cell(myTable, 1, 2, str.tostring(volume, "#,###"))
'''
            },
            'label_drawing': {
                'name': 'Label Drawing',
                'description': 'Label drawing example',
                'code': '''
if ta.crossover(ta.sma(close, 10), ta.sma(close, 20))
    label.new(bar_index, low, "BUY", 
              style=label.style_label_up, 
              color=color.green, 
              textcolor=color.white,
              size=size.small)

if ta.crossunder(ta.sma(close, 10), ta.sma(close, 20))
    label.new(bar_index, high, "SELL", 
              style=label.style_label_down, 
              color=color.red, 
              textcolor=color.white,
              size=size.small)
'''
            }
        }
    
    def get_snippet(self, key):
        return self.snippets.get(key, None)
    
    def get_all_snippets(self):
        return self.snippets
