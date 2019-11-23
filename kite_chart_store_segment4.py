import pandas as pd
from CredentialLoader import CredentialLoader
from DhelmChartStore import DhelmChartStore


cred = CredentialLoader()
api_key = cred.get_api_key()
access_token = cred.get_access_token()

df_scrip_list = pd.read_excel('chart_store/chart_store_segment4.xlsx')

for index, row in df_scrip_list.iterrows():
    try:
        DhelmChartStore(row, api_key, access_token)
    except Exception:
        pass
