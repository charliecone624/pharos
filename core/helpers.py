from enum import Enum
from functools import partial
import os
import requests
from requests import Response
from typing import Any, Callable

from numpy.typing import ArrayLike
import pandas as pd

from . import api
from .ticker import Ticker, Components

"""API module functions"""
def get_key(directory: str) -> tuple:
    target = 'key.txt'
    path = os.path.join(directory, target)
    with open(path) as file:
        head, key = file.read().split('=')
    return head, key

def make_endpoint(source: api.Source, *args, **kwargs) -> str:
    resource = '/'.join(args)
    path = f'{source.host}/{resource}'
    if not kwargs:
        return path
    else:
        params = '&'.join([f'{key}={value}' for key, value in kwargs.items()]) if kwargs else None
        return f'{path}?{params}'

def validate(response: Response) -> None:
    try:
        if response.status_code == 200:
            print('Request successful.')
        else:
            raise Exception(f'Request returned invalid response code: {response.status_code}.')
    except:
        raise Exception('Request failed to return a valid response.')

Parser = Callable[[Response], Any]
"""
A Parser is a strategy that deals with requests in various ways according to the response data structure.
Specifically, this module will define unique Parsers for json and csv responses.

ToDo: Add logic to convert columns to their appropriate data-types for plotting and filtering purposes.
Experiments with df.infer_objects() and df.convert_dtypes() unsuccessful due to data heterogenity. 
Likely will need to implement a series of try/except clauses to check for ints, floats, strs, datetimes for each column.
"""

def parse_json(r: Response) -> dict:
    return r.json()

def parse_json_branch(r: Response, branch: str) -> pd.DataFrame:
    return pd.DataFrame(r.json()[branch])

def parse_csv(r: Response) -> pd.DataFrame:
    data = [i.decode('utf8').split(',') for i in r.iter_lines() if len(i) > 0]
    headers = data.pop(0)
    return pd.DataFrame(data, columns = headers)


"""Portfolio module functions."""

State = Enum('State', 'active delisted')
Horizon = Enum('Horizon', '3month 6month 12month')

def get_listings(state = State['active']) -> ArrayLike:
    assert state in State, f'Please pass a valid listing status:\n{State._member_names_}'

    client = api.Client(api.Source.ALPHA_VANTAGE)
    request = client.get(function = 'LISTING_STATUS', state = state.name)
    return parse_csv(request)

def get_earnings_calendar(horizon = Horizon['3month'], symbol = None) -> ArrayLike:
    assert horizon in Horizon, f'Please pass a valid horizon period:\n{Horizon._member_names_}'

    client = api.Client(api.Source.ALPHA_VANTAGE)
    primed_req = partial(client.get, function = 'EARNINGS_CALENDAR', horizon = horizon.name)
    if symbol:
        request = primed_req(symbol=symbol)
    else:
        request = primed_req()
    return parse_csv(request)

def get_ipo_calendar() -> ArrayLike:
    client = api.Client(api.Source.ALPHA_VANTAGE)
    request = client.get(function = 'IPO_CALENDAR')
    return parse_csv(request)

def get_stock_data(symbol: str) -> Ticker:
    T = Ticker(symbol)
    for i in Components.__members__:
        T.get(Components[i])
    return T

def build_portfolio(tickers: list) -> dict:
    portfolio = {}
    for i in tickers:
        portfolio[i] = get_stock_data(i)
    return portfolio
