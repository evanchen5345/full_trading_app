#! /usr/bin/python

import sqlite3, config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)
assets = api.list_assets()

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")

symbols = [row['symbol'] for row in cursor]

for asset in assets:
    try:
        if asset.symbol not in symbols and asset.status == 'active' and asset.tradable:
            print("Added {} {}".format(asset.symbol, asset.name))
            cursor.execute("INSERT INTO stock (symbol,name) VALUES (?,?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()