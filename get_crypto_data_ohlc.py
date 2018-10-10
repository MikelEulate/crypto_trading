import requests
import pandas as pd

def binance_hist_symbols(list_symbols, interval, limit= 12):
    df = pd.DataFrame()
    for symbol in list_symbols:
 
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        # Get tick by tick data of last price from Binance
        binanceTick = requests.get('https://api.binance.com/api/v1/klines?symbol='+symbol+'&interval='+interval+'&limit='+str(limit))
        hist =  binanceTick.json()
        
        
        open = []
        high = []
        low = []
        close = []

        for i in range(len(hist)):
            #print(hist[i][4])
            open.append(float(hist[i][1]))
            high.append(float(hist[i][2]))
            low.append(float(hist[i][3]))
            close.append(float(hist[i][4]))
            
        df[f'{symbol}_open']= open
        df[f'{symbol}_high']= high
        df[f'{symbol}_low']= low
        df[f'{symbol}_close']= close
    return df


def binance_last_price(symbol): 
    try: 
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        # Get tick by tick data of last price from Binance
        binanceTick = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol)
        return float(binanceTick.json()['price'])
    except:
        return 0
