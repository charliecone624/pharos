from dataclasses import dataclass








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