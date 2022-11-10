import talib as ta
import numpy as np
import ccxt

## I am not your financial adviser, nor is this tool. Use this program as an educational tool, and nothing more. 
## None of the contributors to this project are liable for any losses you may incur. Be wise and always do your own research.

#scores
trend = 0 ## scores higher than 0 indicate uptrend
oversoldoverbought = 0 ## scores higher than 0 indicate oversold(might be good time to buy)
buysell = 0 ## scores higher than 0 indicate buy

exchange = ccxt.binance() ## list of supported exchanges can be found @https://github.com/ccxt/ccxt
timeframe = "4h" ## 1m, 5m, 1h, 4h, 1d, 1M, 1y
eth = "ETH/USDT"
btc = "BTC/USDT" 

data = exchange.fetch_ohlcv(eth, timeframe)

price_open = []
price_high = []
price_low = []
price_close = []
volume = []
for x in data:
    price_open.append(x[1])
    price_high.append(x[2])
    price_low.append(x[3])
    price_close.append(x[4])
    volume.append(x[5])

## convert to np array so readable to ta-lib
po = np.array(price_open)
ph = np.array(price_high)
pl = np.array(price_low)
pc = np.array(price_close)
v = np.array(volume)

def MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, signal, hist = ta.MACD(prices, 
                                    fastperiod=fastperiod, 
                                    slowperiod=slowperiod, 
                                    signalperiod=signalperiod)
    return macd[-1] - signal[-1]

## momentum indicators
rsi = ta.RSI(pc,timeperiod=14)
k, d =  ta.STOCH(rsi, rsi, rsi, 14) ##modified to match trading view stoch rsi values
adx = ta.ADX(ph,pl,pc, 14)
adxr = ta.ADXR(ph,pl,pc, 14)
macd = MACD(pc, fastperiod=12, slowperiod=26, signalperiod=9)
bop = ta.BOP(po, ph, pl, pc)
mfi = ta.MFI(ph, pl, pc, v, timeperiod=14)
mom = ta.MOM(pc, timeperiod=10)
apo = ta.APO(pc, fastperiod=12, slowperiod=26, matype=0)
aroonosc = ta.AROONOSC(ph, pl, timeperiod=14)
ppo = ta.PPO(pc, fastperiod=12, slowperiod=26, matype=0)
roc = ta.ROC(pc, timeperiod=10)
willr = ta.WILLR(ph, pl, pc, timeperiod=14)
plusdi = ta.PLUS_DI(ph, pl, pc, timeperiod=14)
minusdi = ta.MINUS_DI(ph, pl, pc, timeperiod=14)

def di():
    global trend
    if minusdi[-1] > plusdi[-1]:
        trend-=1
    if plusdi[-1] > minusdi[-1]:
        trend+=1

def willr_signal():
    global oversoldoverbought
    if willr[-1] > -20:
        oversoldoverbought -= 1
    if willr[-1] < -80:
        oversoldoverbought += 1

def roc_signal():
    global trend
    if roc[-1] > 0:
        trend+=1
    if roc[-1] < 0:
        trend-=1

def ppo_signal():
    global trend
    if ppo[-1] > 0:
        trend+=1
    if ppo[-1] < 0:
        trend-=1

def aroonosc_signal():
    global trend
    if aroonosc[-1] > 0:
        trend+=1
    if aroonosc[-1] < 0:
        trend-=1

def apo_signal():
    global buysell
    if apo[-1] > 0:
        buysell+=1
    if apo[-1] < 0:
        buysell-=1

def mom_signal():
    global buysell
    if mom[-1] > 0:
        buysell+=1
    if mom[-1] < 0:
        buysell-=1

def mfi_signal():
    global oversoldoverbought
    if mfi[-1] > 80:
        oversoldoverbought -= 1
    if mfi[-1] < 20:
        oversoldoverbought += 1

def bop_signal():
    global buysell
    if bop[-1] > 0:
        buysell += 1
    if bop[-1] < 0 :
        buysell -= 1

def macd_signal():
    global buysell
    if macd < 0:
        buysell -= 1
    if macd > 0:
        buysell += 1

def stochrsi_signal(): 
    global buysell
    if k[-1] > 80 and d[-1] > 80 and k[-1] < d[-1]:
        buysell -= 1
    if k[-1] < 20 and d[-1] < 20 and k[-1] > d[-1]:
        buysell += 1

def rsi_signal(): 
    global oversoldoverbought
    global trend
    if rsi[-1] > 70:
        oversoldoverbought -= 1
    if rsi[-1] < 30:
        oversoldoverbought += 1
    if rsi[-1] > 50:
        trend += 1
    if rsi[-1] < 50:
        trend -= 1

def adx_signal():
    global trend
    global buysell
    if adx[-1] > 25:
        di()
    
    if adx[-1] > 25:
        if adx[-1] > adxr[-1]:
            buysell += 1
        if adxr[-1] > adx[-1]:
            buysell -= 1

##def divergence(pc,indicator):
    ##positive divergence price decreasing, indicator increasing
   
    ##negative divergence price increasing, indicator decreasing

willr_signal()
rsi_signal()
stochrsi_signal()
adx_signal()
macd_signal()
bop_signal()
mfi_signal()
mom_signal()
apo_signal()
aroonosc_signal()
ppo_signal()
roc_signal()

print(eth + " " + str(pc[-1]) + " " + timeframe)

print("RSI(14): " + str(rsi[-1]))
print("Stoch RSI(14): " + str(k[-1])+ ", " + str(d[-1]))
print("ADX,ADXR: " + str(adx[-1]) + ", " + str(adxr[-1]))
print("MACD: " + str(macd))
print("BOP: " + str(bop[-1]))
print("MFI: " + str(mfi[-1]))
print("MOM: " + str(mom[-1]))
print("APO: " + str(apo[-1]))
print("AROONOSC: " + str(aroonosc[-1]))
print("PPO: " + str(ppo[-1]))
print("ROC: " + str(roc[-1]))
print("WILLR: " + str(willr[-1]))
print("PLUSDI/MINUSDI: " + str(plusdi[-1]) + ", " + str(minusdi[-1]))

print("---------------------------------------------------------")

if buysell > 0:
    buy_sell_signal = "Buy:" + str(buysell)
elif buysell < 0:
    buy_sell_signal = "Sell:" + str(buysell)
else:
    buy_sell_signal = "no signal"

if trend > 0:
    trend_signal = "Uptrend:" + str(trend)
elif trend < 0:
    trend_signal = "Downtrend:" + str(trend)
else:
    trend_signal = "no signal"

if oversoldoverbought > 0:
    bsob_signal = "Oversold, trend could soon reverse, might be a good time to buy:" + str(oversoldoverbought)
elif oversoldoverbought < 0:
    bsob_signal = "Overbought, trend could soon reverse, might be a good time to sell:" + str(oversoldoverbought)
else:
    bsob_signal = "no signal"

print(buy_sell_signal + "\n" + trend_signal + "\n" + bsob_signal)
