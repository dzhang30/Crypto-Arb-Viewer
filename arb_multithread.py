import random
import threading
import time

import ccxt
import pandas as pd
from IPython.display import display

gateio = ccxt.gateio()
gdax = ccxt.gdax()
binance = ccxt.binance()
bitbank = ccxt.bitbank()
bit2c = ccxt.bit2c()
bitbay = ccxt.bitbay()

exchanges = {
    gateio: ['ETH/BTC', 'LTC/BTC'],
    gdax: ['ETH/BTC', 'LTC/BTC', 'BTC/USD'],
    binance: ['ETH/BTC', 'LTC/BTC'],
    bitbank: ['ETH/BTC', 'LTC/BTC'],
    bit2c: ['BTC/NIS', 'LTC/NIS'],
    bitbay: ['ETH/BTC', 'LTC/BTC']
}


def get_top_of_book(top_bids, top_asks, exchange, symbol):
    book = exchange.fetch_order_book(symbol)
    top_bids[exchange.name][symbol] = float(book['bids'][0][0])
    top_asks[exchange.name][symbol] = float(book['asks'][0][0])


def get_arb_table(top_of_book):
    df = pd.DataFrame.from_dict(top_of_book)
    cheapest = df.idxmax(1)
    richest = df.idxmin(1)

    df['cheapest'] = cheapest
    df['richest'] = richest

    def calculate_spread(x):
        x1 = x[x['richest']]
        x2 = x[x['cheapest']]
        pct_diff = 100 * (abs(x1 - x2)) / ((x1 + x2) / 2)
        return pct_diff

    df['spread'] = df.apply(calculate_spread, axis=1)
    return df


def run():
    top_bids = {}
    top_asks = {}

    threads = []
    i = 0
    for exchange in exchanges:
        if exchange.name not in top_bids:
            top_bids[exchange.name] = {}
        if exchange.name not in top_asks:
            top_asks[exchange.name] = {}
        for symbol in exchanges[exchange]:
            threads.append(threading.Thread(target=get_top_of_book, args=(top_bids, top_asks, exchange, symbol)))
            threads[i].start()
            i += 1

    for i in range(len(threads)):
        threads[i].join()

    display(get_arb_table(top_bids))
    display(get_arb_table(top_asks))


if __name__ == '__main__':
    start = time.time()
    run()
    print(time.time() - start)
