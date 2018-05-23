import time

import ccxt
import pandas as pd
from IPython.display import display

gateio = ccxt.gateio()
gdax = ccxt.gdax()
# kraken = ccxt.kraken()
binance = ccxt.binance()
bitbank = ccxt.bitbank()
bit2c = ccxt.bit2c()
bitbay = ccxt.bitbay()

exchanges = {
    gateio: ['ETH/BTC', 'LTC/BTC'],
    gdax: ['ETH/BTC', 'LTC/BTC', 'BTC/USD'],
    # kraken: ['ETH/BTC', 'LTC/BTC', 'BTC/USD'],
    binance: ['ETH/BTC', 'LTC/BTC'],
    bitbank: ['ETH/BTC', 'LTC/BTC'],
    bit2c: ['BTC/NIS', 'LTC/NIS'],
    bitbay: ['ETH/BTC', 'LTC/BTC']

}


def get_top_of_book(exchange, symbol):
    book = exchange.fetch_order_book(symbol)
    best_bid_price = book['bids'][0][0]
    best_ask_price = book['asks'][0][0]
    return best_bid_price, best_ask_price


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
    for exchange in exchanges:
        if exchange.name not in top_bids:
            top_bids[exchange.name] = {}
        if exchange.name not in top_asks:
            top_asks[exchange.name] = {}

        for symbol in exchanges[exchange]:
            best_bid_price, best_ask_price = get_top_of_book(exchange, symbol)
            top_bids[exchange.name][symbol] = float(best_bid_price)
            top_asks[exchange.name][symbol] = float(best_ask_price)

    display(get_arb_table(top_bids))
    display(get_arb_table(top_asks))


if __name__ == '__main__':
    start = time.time()
    run()
    print(time.time() - start)
