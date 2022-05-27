import os
import pickle
from dataclasses import dataclass, field
from functools import partial
from enum import Enum

from numpy.typing import ArrayLike

from . import api
from .api import Client, Source, call

class Components(Enum):
    overview = ('OVERVIEW', api.parse_json)
    balance_sheet = ('BALANCE_SHEET', partial(api.parse_json_branch, branch = 'quarterlyReports'))
    income_statement = ('INCOME_STATEMENT', partial(api.parse_json_branch, branch = 'quarterlyReports'))
    cash_flow = ('CASH_FLOW', partial(api.parse_json_branch, branch = 'quarterlyReports'))
    earnings = ('EARNINGS', partial(api.parse_json_branch, branch = 'quarterlyEarnings'))

    def __init__(self, endpoint, func):
        self.parser = func
        self.endpoint = endpoint

    def parse(self, request):
        return self.parser(request)

@dataclass
class Ticker:
    symbol: str
    client = Client(Source.ALPHA_VANTAGE)

    overview: ArrayLike = field(init=False, default=None)
    balance_sheet: ArrayLike = field(init=False, default=None)
    income_statement: ArrayLike = field(init=False, default=None)
    cash_flow: ArrayLike = field(init=False, default=None)
    earnings: ArrayLike = field(init=False, default=None)

    def get(self, comp: Components):
        request = comp.endpoint
        raw = self.client.get(function = request, symbol = self.symbol)
        parsed = comp.parse(raw)
        setattr(self, comp.name, parsed)
    
    def write(self):
        file_name = f'{os.path.join(Source.ALPHA_VANTAGE.local, "tickers", self.symbol)}.pkl'
        with open(file_name, 'ab') as file:
            pickle.dump(self, file)
            file.close()

    def format(self, comp: Components):
        data = getattr(self, comp.name)
        if data:
            return api.format(data, ('Symbol', self.symbol))

    def read(self):
        pass
