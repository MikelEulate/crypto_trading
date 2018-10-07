import time, json, requests, smtplib
import datetime
import pandas as pd


## exchanges to trade on: Coinbase, ExStock, LiveCoin, OkCoin, Bittrex, Bitfinex, Bitstamp, Pololinex

bitfinex_market = 'ltcusd'
# bittrex_market = 'USD-ETH' % bittrex exchange do not have ltc-usd trading pair
kraken_market = 'XETHZUSD'
#bitlish_market = 'ethusd'
bitlish_market = bitfinex_market
coinbase_market = 'LTC-USD'
livecoin_market = 'LTC/USD'
okcoin_market = 'ltc_usd'
bitstamp_market = bitfinex_market
pololinex_market = 'USDT_LTC'

fee = [0.0025, 0.0025]

chat = 0
equity = 600
    
    
    

# Helper functions
def bitfinex():
    try:
        # Get tick by tick data of last price from Bitfinex
        # https://www.bitfinex.com/pages/api
        bitFinexTick = requests.get("https://api.bitfinex.com/v1/ticker/"+bitfinex_market)
        return bitFinexTick.json()['last_price']
    except:
        return 0

def bittrex(): 
    try: 
        # Get tick by tick data of last price from Bittrex
        # https://support.bittrex.com/hc/en-us/articles/115003723911
        bittrexTick = requests.get("https://bittrex.com/Api/v1.1/public/getmarketsummary?market="+bittrex_market)
        return bittrexTick.json()['result'][0]['Last']
    except:
        return 0

def kraken():
    try:
         # Get tick by tick data of last price from Kraken
         # https://www.kraken.com/help/api
        #krakenTick = requests.post('https://api.kraken.com/0/public/Ticker',
        #                           data=json.dumps({"pair":kraken_market}),
        #    headers={"content-type":"application/json"})
        #return krakenTick.json()['result'][kraken_market]['c'][0]
        
        krakenTick = requests.get("https://api.kraken.com/0/public/Ticker?pair="+kraken_market)
        return krakenTick.json()['result'][kraken_market]['c'][0]
    except:
        return 0

def bitlish():
    try:
        # Get tick by tick data of last price from Bitlish
        # https://bitlish.com/api
        bitlishTick = requests.get("https://bitlish.com/api/v1/tickers")
        return bitlishTick.json()[bitlish_market]['last']
    except:
        return 0
        
        
def coinbase():
    try:
        # Get tick by tick data of last price from Coinbase
        # https://developers.coinbase.com/api/v2
        coinbaseTick = requests.get("https://api.coinbase.com/v2/prices/"+coinbase_market+"/spot")
        return coinbaseTick.json()['data']['amount']
    except:
        return 0

def livecoin():
    try:
        # Get tick by tick data of last price from Livecoin
        # https://api.livecoin.net/exchange/
        livecoinTick = requests.get("https://api.livecoin.net/exchange/ticker?currencyPair="+livecoin_market)
        return livecoinTick.json()['last']
    except:
        return 0
    
def okcoin():
    try:
        # Get tick by tick data of last price from OKCoin
        # https://support.okcoin.com/hc/en-us/articles/360000697832-REST-API-Reference
        okcoinTick = requests.get("https://www.okcoin.com/api/v1/ticker.do?symbol="+okcoin_market)
        return okcoinTick.json()['ticker']['last']
    except:
        return 0    

def bitstamp():
    try:
        # Get tick by tick data of last price from Bitstamp
        # https://www.bitstamp.net/api/
        bitstampTick = requests.get("https://www.bitstamp.net/api/v2/ticker/"+bitstamp_market+"/")
        return bitstampTick.json()['last_price']
    except:
        return 0  
    
def pololinex():
    try:
        # Get tick by tick data of last price from Pololinex
        # https://poloniex.com/support/api/
        pololinexTick = requests.get("https://poloniex.com/public?command=returnTicker")
        return pololinexTick.json()[pololinex_market]['last']
    except:
        return 0 


## Crypto Telegram Bot

TOKEN = ""
URL = ""


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
    

def inicio_logs():
    text = 'Starting the Stat Arb Trading with ETH-USD in real time'
    send_message(text, chat)
    
    text = 'Trading Now: '+coinbase_market
    send_message(text, chat)
    
    
    krakenUSDLive = float(kraken())
    text = 'Kraken Price: ' + str(krakenUSDLive)
    send_message(text, chat)
    
    bitfinexUSDLive = float(bitfinex())
    text = 'Bitfinex Price: '+ str(bitfinexUSDLive)
    send_message(text, chat)
    
    bittrexUSDLive = float(bittrex())
    text = 'Bittrex Price: ' + str(bittrexUSDLive)
    send_message(text, chat)
    
    bitlishUSDLive = float(bitlish())
    text = 'Bitlish Price: ' + str(bitlishUSDLive)
    send_message(text, chat)
    
    coinbaseUSDLive = float(coinbase())
    text = 'Coinbase Price: '+ str(coinbaseUSDLive)
    send_message(text, chat)
    
    
    
if __name__ == '__main__':
    
    exchange1_pnl = []
    exchange2_pnl = []
    trading_log = []
    acc1 = 0.5*equity # 50% of base capital in exch 1
    acc2 = 0.5*equity
    roi = []   
    cash_ex1 = []
    cash_ex2 = []
    
    inicio_logs()
    
    coinbaseLive = float(coinbase())
    print('coinbase: ', coinbaseLive)
    liveCoinLive = float(livecoin())
    print('liveCoin: ', liveCoinLive)
    okcoinLive = float(okcoin())
    print('okcoin: ', okcoinLive)
    bitfinexLive = float(bitfinex())
    print('bitfinex: ', bitfinexLive)
    bitstampLive = float(bitstamp())
    print('bitstamp: ', bitstampLive)
    pololinexLive = float(pololinex())
    print('pololinex: ', pololinexLive)
    
    columns = ['timestamp','coinbase', 'liveCoin', 'okcoin', 'bitfinex', 'bitstamp', 'pololinex']

    df_eth = pd.DataFrame(columns=columns)
    
    columns_account = ['timestamp','exchange1_pnl', 'exchange2_pnl', 'cash_ex1', 'cash_ex2', 'trading_log']

    df_acc = pd.DataFrame(columns=columns_account)

    i = 0

    pos = None
    while True:
        
        coinbaseLive = float(coinbase())
        liveCoinLive = float(livecoin())
        okcoinLive = float(okcoin())
        bitfinexLive = float(bitfinex())
        bitstampLive = float(bitstamp())
        pololinexLive = float(pololinex())
        
        k = datetime.datetime.now()
        print('Timestamp: ', k)
        
        df1_cp = float(livecoin())
        print('LiveCoin LTC-USD Price:', df1_cp)
        df2_cp = float(bitfinex())
        print('Bitfinex LTC-USD Price:', df2_cp)
        diff = df1_cp - df2_cp
        print('Difference:', diff)
        
        min_balance = min(acc1, acc2) # Trade on this capital
        if min_balance < 50: # Terminate strategy and exit the market.
            break
       
        if pos is None: 
            if diff < -0.025*min(df1_cp, df2_cp):
                
                # Open long
                adjusted_df1_cp = df1_cp + df1_cp*fee[0]
                no_of_coins = round(min_balance/ adjusted_df1_cp, 3)
                long_invst = no_of_coins*adjusted_df1_cp
                    
                adjusted_df2_cp = df2_cp + df2_cp*fee[1]
                short_invst = no_of_coins*adjusted_df2_cp
                
                msg_1 = '\n' + 'Potential LTC long spread: Bitlish and Bitfinex.'
                msg_1 = msg_1 + '\n' + 'Long Bitlish and short Bitfinex.' + "\n"
                print(msg_1)
                send_message(msg_1, chat)
                 
                pos = 'Long'
                msg = "Long position opened with " + str(no_of_coins) + " number of coins."
                trading_log = msg
                
                print(msg)
                send_message(msg, chat)
        
            if diff > 0.025*min(df1_cp, df2_cp):
                # Open Short
                adjusted_df2_cp = df2_cp + df2_cp*fee[1]
                no_of_coins = round(min_balance/ adjusted_df2_cp, 3)
                long_invst = no_of_coins*adjusted_df2_cp
                    
                adjusted_df1_cp = df1_cp + df1_cp*fee[0]
                short_invst = no_of_coins*adjusted_df1_cp
                
                msg_1 = '\n' + 'Potential LTC short spread: Bitlish and Bitfinex.'
                msg_1 = msg_1 + '\n' + 'Short Bitlish and long Bitfinex.' + "\n"
                print(msg_1)
                send_message(msg_1, chat)
                    
                pos = 'Short'
                msg = "Short position opened with " + str(no_of_coins) + " number of coins."
                trading_log = msg
                
                print(msg)
                send_message(msg, chat)

        if pos is not None:  
            if pos == 'Long' and diff >= 0.01*min(df1_cp, df2_cp):
                # Close long and update trade statstics
                adjusted_df1_cp = df1_cp - df1_cp*fee[0]
                exchange1_profit = no_of_coins*adjusted_df1_cp - long_invst
                exchange1_pnl = exchange1_profit
                acc1 += exchange1_profit
                acc1 = round(acc1, 2)
                cash_ex1 = acc1
                
                adjusted_df2_cp = df2_cp - df2_cp*fee[1]
                exchange2_profit = -no_of_coins*adjusted_df2_cp + short_invst
                exchange2_pnl = exchange2_profit
                acc2 += exchange2_profit
                acc2 = round(acc2, 2)
                cash_ex2 = acc2
                
                msg_1 = '\n' + 'Close LTC long spread: Bitlish and Bitfinex.'
                msg_1 = msg_1 + '\n' + 'Close the Bitlish long and Bitfinex short.'+ "\n"
                print(msg_1)
                send_message(msg_1, chat)
                    
                msg = 'Long position closed with net profit ' + '{}$'.format(exchange1_profit + exchange2_profit)
                print(msg)
                send_message(msg, chat)
                trading_log = msg
                pos = None

            if pos == 'Short' and diff <= -0.01*min(df1_cp, df2_cp):
                # Close Short and update trade statistics
                adjusted_df2_cp = df2_cp - df1_cp*fee[1]
                exchange2_profit = no_of_coins*adjusted_df2_cp - long_invst
                exchange2_pnl = exchange2_profit
                acc2 += exchange2_profit
                acc2 = round(acc2, 2)
                cash_ex2 = acc2
                   
                adjusted_df1_cp = df1_cp - df1_cp*fee[0]
                exchange1_profit = -no_of_coins*adjusted_df1_cp + \
                                       short_invst
                exchange1_pnl = exchange1_profit
                acc1 += exchange1_profit
                acc1 = round(acc1, 2)
                cash_ex1 = acc1
                
                msg_1 = '\n' + 'Close LTC short spread: Bitlish and Bitfinex' 
                msg_1 = msg_1 + '\n' + 'Close the Bitlish short and Bitfinex long.' + "\n"
                print(msg_1)
                send_message(msg_1, chat)
                    
                msg = 'Short position closed with net profit ' + \
                            '{}$ '.format(exchange1_profit + exchange2_profit)
                print(msg)
                send_message(msg, chat)
                trading_log = msg

                pos = None

                
        print('--------------------------------------------')
        d = {'timestamp': [k], 'coinbase': [coinbaseLive], 'liveCoin' : [liveCoinLive],\
         'okcoin' : [okcoinLive], 'bitfinex' : [bitfinexLive], 'bitstamp' : [bitstampLive], 'pololinex' : [pololinexLive]}
        df1_eth = pd.DataFrame(data=d)
        df_eth = df_eth.append(df1_eth)
        
        a = {'timestamp': [k], 'exchange1_pnl': [exchange1_pnl], 'exchange2_pnl' : [exchange2_pnl],\
         'cash_ex1' : [cash_ex1], 'cash_ex2' : [cash_ex2], 'trading_log' : [trading_log]}
        df1_acc = pd.DataFrame(data=a)
        df_acc = df_acc.append(df1_acc)
        
        if i % 10 == 0:
            try:
                print('Timestamp: ', k)
                msg = 'Timestamp: ' + str(k)
                msg = msg + '\n' + 'Saving the logs info' + "\n"
                #send_message(msg, chat)
                df_eth.to_csv('df_ltc.csv')
                df_acc.to_csv('df_acc_ltc.csv')
            except:
                pass
        i = i +1
        s = (datetime.datetime.now() - k).seconds
        time.sleep(300-int(s))
    
    
    
    
    
