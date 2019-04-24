# import logging
import pandas as pd
from instrument_list_downloader import list_downloader
from CredentialLoader import CredentialLoader
# from Credentials import credentials
"""
This script is to be used to dump all instrument lists in different exchanges.
# Command to run py kite_instrument_list_dumper.py
"""
cred = CredentialLoader()
api_key = cred.get_api_key()
access_token = cred.get_access_token()
list_downloader(api_key, access_token, 'NSE')
list_downloader(api_key, access_token, 'MCX')
list_downloader(api_key, access_token, 'NFO')
data_nse = pd.read_csv('instruments/NSE.csv')
data_fno = pd.read_csv('instruments/NFO.csv')
all_fno_list = pd.DataFrame(columns=['exchange',
                                     'exchange_token',
                                     'expiry',
                                     'instrument_token',
                                     'instrument_type',
                                     'last_price',
                                     'lot_size',
                                     'name',
                                     'segment',
                                     'strike',
                                     'tick_size',
                                     'tradingsymbol'])
list_tradingsymbols_fno = data_fno['tradingsymbol'].tolist()
for index, row in data_nse.iterrows():
    print('Checking ' + row['tradingsymbol'])
    for i in range(len(list_tradingsymbols_fno)):
        if row['tradingsymbol'] in list_tradingsymbols_fno[i]:
            all_fno_list.loc[len(all_fno_list)] = row
            break

all_fno_list.to_csv('instruments/all_fno_list.csv', encoding='utf-8', index=False)
