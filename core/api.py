from enum import Enum
import os
import requests

from .helpers import get_key, make_endpoint, validate

class Source(Enum):
    """
    Contains data provider names and domains to be used within existing and developing Pharos functionality.
        :param host: top-level https domain
        :param local: name of directory to store Source-related files such as api-keys 
                        and output data. 
    """

    ALPHA_VANTAGE = ('https://www.alphavantage.co/query', 'alpha vantage')
    BEA = ('https://apps.bea.gov/api/data', 'bureau of economic analysis')
    EPA = ('https://data.epa.gov/efservice', 'environmental protection agency')
    BLS = ('https://api.bls.gov/publicAPI/v2/timeseries/data/', 'bureau of labor statistics')

    def __init__(self, host: str, local: str):
        self.host = host
        self.local = os.path.join(r'C:\Users\charl\OneDrive\resources', local)

class Client:
    """
    Constructor object used to execute http requests.
    """
    def __init__(self, source: Source):
        self.source = source

    def get(self, *args, **kwargs):
        try:
            head, key = get_key(self.source.local)
            kwargs[head] = key
        except:
            print(f'No key found for {self.source.name}')
        endpoint = make_endpoint(self.source.local, *args, **kwargs)
        print(f'Calling: {endpoint}...')
        
        response = requests.get(endpoint)
        validate(response)
        
        return response