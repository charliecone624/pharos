import os
import time
from multiprocessing import Pool
from functools import partial
from typing import Callable
from datetime import datetime as dt

import pandas as pd

from data import api, ticker, market
from data.ticker import Ticker, Components

def etl_ticker(t: Ticker, root = r'C:\Users\charl\OneDrive\resources\alpha_vantage\tickers'):
    for el in Components:
        data = getattr(t, el.name, None)
        if data is None:
            t.get(el)
        else:
            continue
    t.write(root)
    return t

def get_and_format(t: Ticker, comp: Components):
    t.get(comp)
    return t.format(comp)

def etl_component(tickers: list[Ticker], comp: Components, root = r'C:\Users\charl\OneDrive\resources\alpha_vantage\components'):
    results = []
    with Pool(processes = 4) as pool:
        for t in tickers:
            results.append(pool.apply_async(get_and_format, args = (t, comp)))
            time.sleep(1)
        pool.close()
        pool.join()
    comp_df = pd.concat([r.get() for r in results])
    file = f'{os.path.join(root, comp.name)}.csv'
    comp_df.to_csv(file)
    return comp_df

def main():
    start = dt.now()
    listings = market.get_listings()
    nyse = listings.loc[(listings.assetType=='Stock') & (listings.exchange.isin(['NYSE','NASDAQ'])), 'symbol']
    ticks = [Ticker(sym) for sym in nyse.unique()]
    etl_component(ticks, Components.overview)
    print(dt.now()-start)

if __name__ == '__main__':
    main()