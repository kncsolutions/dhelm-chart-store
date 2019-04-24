import logging
from kiteconnect import KiteConnect
from kiteconnect import exceptions
from collections import OrderedDict, Counter
import pandas as pd
import datetime
import requests

"""

"""
logging.basicConfig(level=logging.DEBUG)


class historical_data_downloader:
    def __init__(self, api_key, access_token, exchange, tradingsymbol, from_dt, to_dt=str(datetime.datetime.now()),
                 data_time_frame='day', continuous=False):
        self.kite = KiteConnect(api_key)
        self.kite.set_access_token(access_token)
        self.df = pd.DataFrame()
        data = pd.read_csv('instruments/' + exchange + '.csv')
        instrument_token = data['instrument_token'].tolist()
        symbol = data['tradingsymbol'].tolist()
        i_token = instrument_token[symbol.index(tradingsymbol)]
        print('instrument token for ' + tradingsymbol + ' is ' + str(i_token))
        hist = None
        try:
            hist = self.kite.historical_data(i_token, from_dt, to_dt, data_time_frame, continuous)
        except requests.exceptions.ReadTimeout:
            pass
        except exceptions.NetworkException:
            pass
        except Exception:
            pass
        # print(hist)
        if hist is not None:
            for entry in hist:
                if 'date' in entry:
                    entry['date'] = str(entry['date'])

            # print(hist)

            col = Counter()
            for k in list(hist):
                col.update(k)
                self.df = pd.DataFrame([k.values() for k in hist], columns=col.keys())

    """
	"""

    def get_historical_data(self):
        return self.df
