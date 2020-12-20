#! /usr/bin/python

import sqlite3
import alpaca_trade_api as tradeapi
from config import API_KEY, SECRET_KEY

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets', api_version='v2')
assets = api.list_assets()

print("next")

connection = sqlite3.connect('/Users/evanchen/Desktop/Projects/Stocks/Full-Trading-App/app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, company FROM stock
""")

symbols = [row['symbol'] for row in cursor]

for asset in assets:
    try:
        if asset.symbol not in symbols and asset.status == 'active' and asset.tradable:
            print("Added {} {}".format(asset.symbol, asset.name))
            cursor.execute("INSERT INTO stock (symbol,company) VALUES (?,?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()