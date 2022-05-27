from enum import Enum
import os
from urllib.parse import urljoin
import requests
from requests import Response
from functools import partial, singledispatch
from typing import Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime as dt
from abc import ABC, abstractmethod

import pandas as pd

class Source(Enum):
    ALPHA_VANTAGE = ('https://www.alphavantage.co/query', 'alpha vantage')
    BEA = ('https://apps.bea.gov/api/data', 'bureau of economic analysis')
    EPA = ('https://data.epa.gov/efservice', 'environmental protection agency')
    BLS = ('https://api.bls.gov/publicAPI/v2/timeseries/data/', 'bureau of labor statistics')

    def __init__(self, host: str, local: str):
        self.host = host
        self.local = os.path.join(r'C:\Users\charl\OneDrive\resources', local)

def get_key(directory: str) -> tuple:
    target = 'key.txt'
    path = os.path.join(directory, target)
    with open(path) as file:
        head, key = file.read().split('=')
    return head, key

def make_endpoint(source: Source, *args, **kwargs):
    resource = '/'.join(args)
    path = f'{source.host}/{resource}'
    if not kwargs:
        return path
    else:
        params = '&'.join([f'{key}={value}' for key, value in kwargs.items()]) if kwargs else None
        return f'{path}?{params}'

def call(source: Source, *args, **kwargs):
    try:
        head, key = get_key(source.local)
        kwargs[head] = key
    except:
        print(f'No key found for {source.name}')
    call = make_endpoint(source, *args, **kwargs)
    print(call)
    return requests.get(call)

Parser = Callable[[Response], Any]
"""
A Parser is a strategy that deals with requests in various ways according to the response data structure.
Specifically, this module will define unique Parsers for json and csv responses.
"""

def parse_json(r: Response) -> dict:
    return r.json()

def parse_json_branch(r: Response, branch: str) -> pd.DataFrame:
    return pd.DataFrame(r.json()[branch])

def parse_csv(r: Response) -> pd.DataFrame:
    data = [i.decode('utf8').split(',') for i in r.iter_lines() if len(i) > 0]
    headers = data.pop(0)
    return pd.DataFrame(data, columns = headers)

Formatter = Callable[[Any, Any], pd.DataFrame]
"""
A Formatter is a strategy that transforms data returned by parsers for integration in broader-scoped datasets.
"""

@singledispatch
def format(X, ref):
    pass

@format.register
def _(X: pd.DataFrame, ref: Tuple):
    header, key = ref
    stacked = X.stack().reset_index()
    stacked.columns = ['item', 'value']
    stacked[header.lower()] = key
    return stacked

@format.register
def _(X: dict, ref: Tuple):
    header, key = ref
    if header not in X.keys(): 
        print(f'{header} not in {key}')
        return pd.DataFrame()
    key = X.pop(header)
    formatted = pd.DataFrame({k: [v] for k,v in X.items()})
    formatted[header.lower()] = key
    formatted.set_index(header.lower(), inplace=True)
    return formatted

class Client:

    def __init__(self, source: Source):
        self.source = source

    def get(self, *args, **kwargs):
        request = call(self.source, *args, **kwargs)
        
        try:
            if request.status_code == 200:
                print('Request successful.')
            else:
                raise Exception(f'Request returned invalid response code: {request.status_code}.')
        except:
           raise Exception('Request failed to return a response.')
        
        return request