from dataclasses import dataclass, InitVar

import pandas as pd

from .ticker import Components
from .utilities import build_portfolio

@dataclass
class Portfolio:
    """
    A collection of Tickers. Used for comparative analysis.
        :param symbols: list of valid NYSE or NASDAQ symbols pertaining to public entities or ETFs.
    """
    symbols: InitVar(list) = []

    def __post_init__(self, symbols):
        self.raw_data = build_portfolio(symbols)

    def __group_ticker_data__(self, c: Components) -> pd.DataFrame:
        grouped = pd.DataFrame()
        for T in self.raw_data.keys():
            df = getattr(self.raw_data[T], c.name)
            df['Symbol'] = T
            assert type(df) == pd.DataFrame, f'Ticker component: {c.name} is not a valid DataFrame.'
            grouped = pd.concat([grouped, df])
        return grouped.groupby('Symbol')

    @property
    def overview(self):
        return pd.DataFrame([self.raw_data[T].overview for T in self.raw_data.keys()])
    
    @property
    def balance_sheet(self):
        return self.__group_ticker_data__(Components.balance_sheet)
    
    @property
    def earnings(self):
        return self.__group_ticker_data__(Components.earnings)
    
    @property
    def income_statement(self):
        return self.__group_ticker_data__(Components.income_statement)
    
    @property
    def cash_flow(self):
        return self.__group_ticker_data__(Components.cash_flow)
