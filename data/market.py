from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Union

from numpy.typing import ArrayLike
import pandas as pd

import data.api as api
from data.api import Source, parse_csv, call

State = Enum('State', 'active delisted')
Horizon = Enum('Horizon', '3month 6month 12month')

def get_listings(state = State['active']) -> ArrayLike:
    assert state in State, f'Please pass a valid listing status:\n{State._member_names_}'

    client = api.Client(Source.ALPHA_VANTAGE)
    request = client.get(function = 'LISTING_STATUS', state = state.name)
    return parse_csv(request)

def get_earnings_calendar(horizon = Horizon['3month'], symbol = None) -> ArrayLike:
    assert horizon in Horizon, f'Please pass a valid horizon period:\n{Horizon._member_names_}'

    client = api.Client(Source.ALPHA_VANTAGE)
    primed_req = partial(client.get, function = 'EARNINGS_CALENDAR', horizon = horizon.name)
    if symbol:
        request = primed_req(symbol=symbol)
    else:
        request = primed_req()
    return parse_csv(request)

def get_ipo_calendar() -> ArrayLike:
    client = api.Client(Source.ALPHA_VANTAGE)
    request = client.get(function = 'IPO_CALENDAR')
    return parse_csv(request)

@dataclass
class Industry:
    alpha_vantage_name: str
    tickers: str
    

# class Market(dict):
#     def __init__(init: Union[str,pd.DataFrame]):
#         if type(init) == str:
#             df = pd.read_csv(path, index_col='Symbol')
#         elif type(init) == pd.DataFrame:
#             df = init
#         else:
#             raise Exception('TypeError')
        
        # self.