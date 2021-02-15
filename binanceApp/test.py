import os

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client('MIPFco456I2i3nSBeV6NnZUSYP3Bb8r4zejs9cHYf5dOAyxHDMo4bYbURkQGlaMn',
                'fdYtZD0hNqfQbMqKrcM5e5viqb8TYTV8AotCdGoRPxuvQcFtU5URoxeKah58z3sW',
                )
## main

# create order

# make a test order first. This will raise an exception if the order is incorrect.
buy_order_limit = client.create_test_order(
	symbol='ETHUSDT',
	side='BUY',
	type='LIMIT',
	timeInForce='GTC',
	quantity=100,
price='3.444')

buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)

# create a real order if the test orders did not raise an exception
try:
	buy_limit = client.create_order(
		symbol='ETHUSDT',
		side='BUY',
		type='LIMIT',
		timeInForce='GTC',
		quantity=100,
		price=200)

	# same order but with helper function
	buy_limit = client.order_limit_buy(symbol='ETHUSDT', quantity=100, price=200)

	# market order using a helper function
	market_order = client.order_market_sell(symbol='ETHUSDT', quantity=100)

	# cancel previous orders
	cancel = client.cancel_order(symbol='ETHUSDT', orderId=buy_limit['orderId'])
except BinanceAPIException as e:
	# error handling goes here
	print(e)
except BinanceOrderException as e:
	# error handling goes here
	print(e)

# using binance constants - the library has hard coded commonly used strings
# https://python-binance.readthedocs.io/en/latest/constants.html#

# this order uses required strings such as 'BUY' and 'MARKET' which are prone to spelling errors
buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)

# binance constants can be used instead
buy_order = client.create_test_order(symbol='ETHUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=100)