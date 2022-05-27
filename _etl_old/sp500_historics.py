# #!/usr/bin/env python
# # coding: utf-8

# # In[7]:


# import time
# import requests
# import random
# import string

# import pandas as pd

# from ApiCall import ApiCall, execute


# # In[11]:


# def get_av_keys() -> list:
#     with open('av_key.txt') as file:
#         keys = file.read().split()
#     return keys

# def random_str(call: ApiCall) -> requests.Response: 
#     #This takes advantage of a presumed bug in AlphaVantages api that returns valid results for the Extended Intraday History 
#     # endpoint using any str as an api key
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

# def get_historic_stock_data(call: ApiCall) -> requests.Response:
#     keys = get_av_keys()
#     i = 0
#     for key in keys:
#         signed_call = f'{call.path}&apikey={key}'
#         response = requests.get(signed_call)     
#         if response.status_code != 200 and i <= len(keys):
#             keys.pop(key)
#             keys.append(random_str())
#             print('Invalid API key - daily limit likely reached. Moving onto next key.')
#             i += 1
#             continue
#         else:
#             return response
        
#     print(f'Check request params. No valid response after {i} attempts.')

# def classify_historic_stock(call: ApiCall) -> str:
#     return f'historics/{call.params["interval"]}/{call.params["symbol"]}/{call.params["slice"]}'


# # In[12]:


# def main():
#     host = 'https://www.alphavantage.co/query'
#     sp500 = pd.read_csv('sp500.csv').Symbol.unique()

#     params = {}
#     params['function'] = 'TIME_SERIES_INTRADAY_EXTENDED'
#     params['interval'] = '15min'
#     for ticker in sp500:
#         params['symbol'] = ticker
#         for y in range(1,3):
#             for m in range(1,13):
#                 params['slice'] = f'year{y}month{m}'
#                 call = ApiCall(host, params)
#                 execute(call, get_historic_stock_data, classify_historic_stock)            
            
# if __name__ == '__main__':
#     main()

