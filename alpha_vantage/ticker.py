import os
import pickle
from dataclasses import dataclass, field
from functools import partial
from enum import Enum

from numpy.typing import ArrayLike

from core import api, etl

class Components(Enum):
    overview = ('OVERVIEW', etl.parse_json)
    balance_sheet = ('BALANCE_SHEET', partial(etl.parse_json_branch, branch = 'quarterlyReports'))
    income_statement = ('INCOME_STATEMENT', partial(etl.parse_json_branch, branch = 'quarterlyReports'))
    cash_flow = ('CASH_FLOW', partial(etl.parse_json_branch, branch = 'quarterlyReports'))
    earnings = ('EARNINGS', partial(etl.parse_json_branch, branch = 'quarterlyEarnings'))

    def __init__(self, endpoint, func):
        self.parser = func
        self.endpoint = endpoint

    def parse(self, request):
        return self.parser(request)

@dataclass
class Ticker:
    symbol: str
    __client__ = api.Client(api.Source.ALPHA_VANTAGE)

    overview: ArrayLike = field(init=False, default=None)
    balance_sheet: ArrayLike = field(init=False, default=None)
    income_statement: ArrayLike = field(init=False, default=None)
    cash_flow: ArrayLike = field(init=False, default=None)
    earnings: ArrayLike = field(init=False, default=None)

    def get(self, comp: Components) -> None:
        request = comp.endpoint
        raw = self.__client__.get(function = request, symbol = self.symbol)
        parsed = comp.parse(raw)
        setattr(self, comp.name, parsed)
    
    def write(self) -> None:
        file_name = f'{os.path.join(api.Source.ALPHA_VANTAGE.local, "tickers", self.symbol)}.pkl'
        with open(file_name, 'ab') as file:
            pickle.dump(self, file)
            file.close()

    def read(self):
        """
        In progress.
        """
        pass
