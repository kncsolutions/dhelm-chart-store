import pandas as pd
from CredentialLoader import CredentialLoader
from DhelmChartStore import DhelmChartStore


cred = CredentialLoader()
api_key = cred.get_api_key()
access_token = cred.get_access_token()
settings = pd.read_excel('chart_store/chart_store_settings.xlsx')
if settings.at[0, 'selective']:
    df_scrip_list = pd.read_excel('chart_store/chart_store_selective.xlsx')
else:
    df_scrip_list = pd.read_excel('chart_store/chart_store_knc_basket.xlsx')
for index, row in df_scrip_list.iterrows():
    try:
        DhelmChartStore(row, api_key, access_token)
    except Exception:
        pass
