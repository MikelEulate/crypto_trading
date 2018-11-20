## This file is created to test the Binance API	and send some orders to the exchange:

import pandas as pd 
import numpy as np 

from binance.client import Client
client = Client(api_key, api_secret)

## ORDER FUNTIONS

# place a test market buy order, to place an actual order use the create_order function
order = client.create_test_order(
    symbol='BNBBTC',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=100)


## Placing a Real order:
from binance.enums import *
order = client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')

## Placing a Limit order:
order = client.order_limit_buy(
    symbol='BNBBTC',
    quantity=100,
    price='0.00001')

order = client.order_limit_sell(
    symbol='BNBBTC',
    quantity=100,
    price='0.00001')

## Placing a Market order:
order = client.order_market_buy(
    symbol='BNBBTC',
    quantity=100)

order = client.order_market_sell(
    symbol='BNBBTC',
    quantity=100)


# Check order status:
order = client.get_order(
    symbol='BNBBTC',
    orderId='orderId')

# Cancel an order:
result = client.cancel_order(
    symbol='BNBBTC',
    orderId='orderId')

# Get open orders: (to be used to filter the trade order signal that if it is already traded an asset do nothing)

orders = client.get_open_orders(symbol='BNBBTC')

orders = client.get_all_orders(symbol='BNBBTC')




## ACCOUNT FUNCTIONS

# Get account info
info = client.get_account()

# Get asset balance
balance = client.get_asset_balance(asset='BTC')

# Get account status
status = client.get_account_status()

# Get trades
trades = client.get_my_trades(symbol='BNBBTC')

# Get trade fees
# get fees for all symbols
fees = client.get_trade_fee()
# get fee for one symbol
fees = client.get_trade_fee(symbol='BNBBTC')
