# Packets needed to be imported:

import pandas as pd
import requests
import time
import json
import datetime
import numpy as np
import statsmodels.tsa.stattools as st
import matplotlib.pyplot as plt
from matplotlib import style

from numpy import isnan, dot
import numpy as np
import pandas as pd
import statsmodels.api as sm

## Portfolio coins with MCAP > 0.5 Billion
crypto_list = ['BTC', 'ETH', 'XRP', 'BCC', 'EOS', 'XLM', 'LTC', 'ADA', 'XMR', 'IOTA', 'DASH',\
 'TRX', 'NEO', 'ETC', 'BNB', 'XEM', 'VET', 'VEN', 'ZEC', 'OMG', 'LSK', 'BCN', 'BCD'] 

lookback = 12        # Period to calculate slope and draw down 12 hours
maxlever = 1.0       # Leverage
profittake = 1.96    # 95% bollinger band for profit take
minimumreturn = 0.1  # Entry if annualized slope is over this level
maxdrawdown = 0.10   # Avoid security with too much drawdown
market_impact = 0.2  # Max order is 10% of market trading volume    
    
weights = {}         # Slope at the time of entry.  0 if not to trade
drawdown = {}        # Draw down at the time of entry
shares = {}


chat = 12611672



list_crypto = ['BTCUSDT',
 'ETHUSDT',
 'XRPUSDT',
 'BCCUSDT',
 'EOSUSDT',
 'XLMUSDT',
 'LTCUSDT',
 'ADAUSDT',
 'XMRBTC',
 'IOTAUSDT',
 'DASHBTC',
 'TRXUSDT',
 'NEOUSDT',
 'ETCUSDT',
 'BNBUSDT',
 'XEMBTC',
 'VETUSDT',
 'VENUSDT',
 'ZECBTC',
 'OMGBTC',
 'LSKBTC',
 'BCNBTC',
 'BCDBTC']


def binance_hist_symbols(list_symbols, interval, limit= 12):
    df = pd.DataFrame()
    for symbol in list_symbols:
 
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        # Get tick by tick data of last price from Binance
        binanceTick = requests.get('https://api.binance.com/api/v1/klines?symbol='+symbol+'&interval='+interval+'&limit='+str(limit))
        hist =  binanceTick.json()
        
        data = []

        for i in range(len(hist)):
            #print(hist[i][4])
            data.append(float(hist[i][4]))
        df[symbol]= data
    return df


def binance_last_price(symbol): 
    try: 
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        # Get tick by tick data of last price from Binance
        binanceTick = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol)
        return float(binanceTick.json()['price'])
    except:
        return 0


def reggresion(df):
    #df = df1['price']
    
    if len(df)> lookback:
        prices = df[(len(df) - lookback):-1]
    else:
        print('DF too short')

    X=range(len(prices))
        
    # Add column of ones so we get intercept
    A=sm.add_constant(X)
    
    for s in df.columns:
        print(s)
        # Price movement
        sd = prices[s].std() 
        #print(sd)
        # Price points to run regression
        Y = prices[s].values
        
        # If all empty, skip
        if isnan(Y).any():
            continue
        
        # Run regression y = ax + b
        results = sm.OLS(Y,A).fit()
        (b, a) =results.params
        #print('b, a', b, a)
        
        # a is daily return.  Multiply by 252 to get annualized trend line slope
        slope = a / Y[-1] * lookback       # Daily return regression * 1 year
        print('SLOPE: ', slope)
        if slope > 0:
            dd = drawdown_calc(Y)
        
        if slope < 0:
            dd = drawdown_calc(-Y)
        
        print('dd', dd)
        # Currently how far away from regression line?
        delta = Y - (dot(a,X) + b)
        #print(delta)
        
        # Don't trade if the slope is near flat 
        slope_min = max(dd, minimumreturn)   # Max drawdown and minimum return 
        #print(slope_min)
        # Current gain if trading
        #gain = get_gain(context, s)
       
        # Exits
        if s in weights and weights[s] != 0:
            # Long but slope turns down, then exit
            if weights[s] > 0 and slope < 0:
                weights[s] = 0
                print('Slope turn bull ' , s)
                text = 'Exiting the Long trade because the slope is turning down'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' positions at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat)  

            # Short but slope turns upward, then exit
            if weights[s] < 0 and 0 < slope:
                weights[s] = 0
                print('Slope turn bear  ', s)
                text = 'Exiting the Short trade because the slope is turning up'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' positions at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 

            # Profit take, reaches the top of 95% bollinger band
            if (delta[-1] > profittake * sd) and (s in weights) and (weights[s] > 0):
                weights[s] = 0        
                print('Long exit ', s)
                text = 'Exiting the Long trade with profit!! :D'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' positions at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 

            # Profit take, reaches the top of 95% bollinger band
            if delta[-1] < - profittake * sd and weights[s] < 0:
                weights[s] = 0        
                print('Short exit ', s)
                text = 'Exiting the Short  trade with profit!! :D'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' positions at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 
        # Entry
        else:
            # Trend is up and price crosses the regression line
            if slope > slope_min and delta[-1] > 0 and delta[-2] < 0 and dd < maxdrawdown:
                weights[s] = slope
                drawdown[s] = slope_min
                print('Long a ', s)
                text = 'Entering a Long Trade!!'
                send_message(text, chat)
                text = 'Buying ' + str(s) + ' at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 

            # Trend is down and price crosses the regression line
            if slope < -slope_min and delta[-1] < 0 and delta[-2] > 0  and dd < maxdrawdown:
                weights[s] = slope
                drawdown[s] = slope_min
                print('Short  a ', s)
                text = 'Entering a Short Trade!!'
                send_message(text, chat)
                text = 'Selling ' + str(s) + ' at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 
               
        ## Stopping for Drawdown reasons:
        if s in weights and weights[s] > 0:
            if dd > drawdown[s]:
                print('Exiting Long position because of stop loss ', s)
                text = 'Exiting Long position because of stop loss'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 
                weights[s] = 0
                #context.shares[s] = 0

        elif s in weights and weights[s] < 0:
            if dd > drawdown[s]:
                print('Exiting Short position because of stop loss ', s)
                text = 'Exiting Short position because of stop loss'
                send_message(text, chat)
                text = 'Closing ' + str(s) + ' at price: ' + str(df[s][len(df_hist)-1])
                send_message(text, chat) 
                weights[s] = 0
                #context.shares[s] = 0
                
                
def drawdown_calc(xs):
    if len(xs) == 0:
        return 0.
    i = np.argmax(np.maximum.accumulate(xs) - xs) # end of the period
    if  len(xs[:i]) == 0:
        return 0.
    j = np.argmax(xs[:i]) # start of period
    return abs((xs[i] - xs[j]) / xs[j])



## Crypto Telegram Bot

TOKEN = "629326723:AAHfDJ7wgeVxUKX7U8ntrj1lNXhXcq9A2v0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    



if __name__ == '__main__':
    
    
    text = 'Starting the Trend Follow Algo Trading in Cryptocurrencies in real time!!!! :D'
    send_message(text, chat)
    
    text = 'Crypto List to follow: '
    send_message(text, chat)
    
    text = "'BTC', 'ETH', 'XRP', 'BCC', 'EOS', 'XLM', 'LTC', 'ADA', 'XMR', 'IOTA', 'DASH',\
 'TRX', 'NEO', 'ETC', 'BNB', 'XEM', 'VET', 'VEN', 'ZEC', 'OMG', 'LSK', 'BCN', 'BCD'"
    send_message(text, chat)
    
    i = 0
    ## Initializing the dataframe with the lookback period:
    
    df_hist = binance_hist_symbols(list_crypto, '1h')
    
    while True:
        k = datetime.datetime.now()
        print('Timestamp: ', k)
        
        line = []
        for crypto in list_crypto:
            symbol_last_price = float(binance_last_price(crypto))
            line.append(symbol_last_price)
            #print('Price: ', symbol_last_price)
        df_hist = df_hist.append(pd.Series(line,index=df_hist.columns.tolist()),ignore_index=True)
        
        reggresion(df_hist)
        
        i = i +1
        if i % 12 == 0:
            df_hist.to_csv('/home/pi/CRYPTO_TRADING/data/crypto_data_trend_follow_algo.csv')
        
        s = (datetime.datetime.now() - k).seconds
        time.sleep(3600-int(s))
    
    
    
