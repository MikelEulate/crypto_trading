## Script to get the balance of the account:

api_key = ''
api_secret = ''

from binance.client import Client
client = Client(api_key, api_secret)

## ACCOUNT FUNCTIONS

# Get account info
info = client.get_account()
# Example response:
"""
{
    "makerCommission": 15,
    "takerCommission": 15,
    "buyerCommission": 0,
    "sellerCommission": 0,
    "canTrade": true,
    "canWithdraw": true,
    "canDeposit": true,
    "balances": [
        {
            "asset": "BTC",
            "free": "4723846.89208129",
            "locked": "0.00000000"
        },
        {
            "asset": "LTC",
            "free": "4763368.68006011",
            "locked": "0.00000000"
        }
    ]
}
"""

# Get asset balance
balance = client.get_asset_balance(asset='BTC')
# Example response:
"""
{
    "asset": "BTC",
    "free": "4723846.89208129",
    "locked": "0.00000000"
}
"""

# Get account status
status = client.get_account_status()
# Example response:
"""
{
    "msg": "Order failed:Low Order fill rate! Will be reactivated after 5 minutes.",
    "success": true,
    "objs": [
        "5"
    ]
}
"""

# Getting the open orders of a symbol (after getting the account info and the balance of the traded cryptos)
orders = client.get_open_orders(symbol='BNBBTC')
## or of all the open orders:
orders = client.get_open_orders()
# Example response:
"""
[
    {
        "symbol": "LTCBTC",
        "orderId": 1,
        "clientOrderId": "myOrder1",
        "price": "0.1",
        "origQty": "1.0",
        "executedQty": "0.0",
        "status": "NEW",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "BUY",
        "stopPrice": "0.0",
        "icebergQty": "0.0",
        "time": 1499827319559
    }
]
"""
