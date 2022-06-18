from enum import Enum
import os
import requests
from requests import Response
from typing import Any, Callable

import pandas as pd

from .api import Source

"""API module functions"""
def get_key(directory: str) -> tuple:
    target = 'key.txt'
    path = os.path.join(directory, target)
    with open(path) as file:
        head, key = file.read().split('=')
    return head, key

def make_endpoint(source: Source, *args, **kwargs) -> str:
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
