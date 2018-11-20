## Script to get the balance of the account:

api_key = ''
api_secret = ''

from binance.client import Client
client = Client(api_key, api_secret)

## ACCOUNT FUNCTIONS

# Get account info
info = client.get_account()

# Get asset balance
balance = client.get_asset_balance(asset='BTC')

# Get account status
status = client.get_account_status()
