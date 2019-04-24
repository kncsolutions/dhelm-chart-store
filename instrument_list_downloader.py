import logging
from kiteconnect import KiteConnect
import pandas as pd
import json
"""

"""
logging.basicConfig(level=logging.DEBUG)


class list_downloader:
	def __init__(self,api_key,access_token,exchange):
		self.kite = KiteConnect(api_key)
		self.kite.set_access_token(access_token)
		instruments = self.kite.instruments(exchange)
		for entry in instruments:
			if 'expiry' in entry:
				entry['expiry'] = str(entry['expiry'])
	
		print(instruments)
		output_dict = json.loads(json.dumps(instruments))
		print(output_dict)
		df1 = pd.DataFrame(output_dict)
		print(df1)
		file_name = 'instruments/'+exchange+'.csv'
		df1.to_csv(file_name, encoding='utf-8', index=False)
