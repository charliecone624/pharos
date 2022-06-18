"""This module contains functions that fetch financial data from the AlphaVantage api."""
from enum import Enum
from functools import partial

from numpy.typing import ArrayLike

from ..core import api, etl
from .ticker import Ticker, Components

State = Enum('State', 'active delisted')
Horizon = Enum('Horizon', '3month 6month 12month')

def get_listings(state = State['active']) -> ArrayLike:
    """Retrieve NYSE and NASDAQ listings.
        :param state: member of enum State that is passed to api endpoint 
    """
    assert state in State, f'Please pass a valid listing status:\n{State._member_names_}'

    client = api.Client(api.Source.ALPHA_VANTAGE)
    request = client.get(function = 'LISTING_STATUS', state = state.name)
    return etl.parse_csv(request)

def get_earnings_calendar(horizon = Horizon['3month'], symbol: str = None) -> ArrayLike:
    """
    Retrieve a specified company earnings calendar.
        :param horizon: member of enum Horizon that is passed to api endpoint
        :param symbol(str, None): str representing valid NASDAQ or NYSE listing to query, 
                                    None value will return earnings calendar for all listings
    """
    assert horizon in Horizon, f'Please pass a valid horizon period:\n{Horizon._member_names_}'

    client = api.Client(api.Source.ALPHA_VANTAGE)
    primed_req = partial(client.get, function = 'EARNINGS_CALENDAR', horizon = horizon.name)
    if symbol:
        request = primed_req(symbol=symbol)
    else:
        request = primed_req()
    return etl.parse_csv(request)

def get_ipo_calendar() -> ArrayLike:
    """
    Retrieve upcoming IPO dates.
    """
    client = api.Client(api.Source.ALPHA_VANTAGE)
    request = client.get(function = 'IPO_CALENDAR')
    return etl.parse_csv(request)

def build_ticker(symbol: str) -> Ticker:
    """
    Constructs Ticker object and calls all datasets specified within enum(Components).
        :param symbol(str): str representing valid NASDAQ or NYSE listing to query
    """
    T = Ticker(symbol)
    for i in Components.__members__:
        T.get(Components[i])
    return T

def build_portfolio(tickers: list[str]) -> dict:
    """
    Creates dictionary of populated Ticker objects from list of symbols.
        :param tickers(list): list of instantiated Ticker objects to query
    """
    portfolio = {}
    for i in tickers:
        portfolio[i] = build_ticker(i)
    return portfolio
