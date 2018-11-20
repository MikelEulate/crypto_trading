## Examples to test in Python:

crypto_list = ['BTCUSDT', 'XRPUSDT', 'ETHUSDT', 'XLMUSDT', 'EOSUSDT', 'LTCUSDT', 'ADAUSDT', 'XMRBTC', 'TRXUSDT', 'DASHBTC', 'BNBUSDT', 'BCCBTC', 'IOTAUSDT']

for crypto in crypto_list:
	if crypto[-4:] == 'USDT':
		print('#####')
		rint('Cryptocurrency: ', crypto, 'with base currency: USDT')
	if crypto[-3:] == 'BTC':
		print('#####')
		print('Cryptocurrency: ', crypto, 'with base currency: BTC')

dash_last_price = 0.022862

btc_price = 4626.69

size_per_currency = 150

number_currencies_to_trade = size_per_currency/(dash_last_price*btc_price)

print(number_currencies_to_trade)
