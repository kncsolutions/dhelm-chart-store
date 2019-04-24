import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd


class CredentialLoader:
    def __init__(self):
        cred = credentials.Certificate("auth/dhelm-kite-autotrader-firebase-adminsdk-kb45y-1818454aae.json")
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://dhelm-kite-autotrader.firebaseio.com'
        })

        # As an admin, the app has access to read and write all data, regradless of Security Rules
        self.ref = pd.DataFrame([db.reference('/credentials/keys').get()])
        print(self.ref)

    def get_api_key(self):
        return self.ref.at[0, 'api_key']

    def get_access_token(self):
        return self.ref.at[0, 'access_token']

    def get_api_secret(self):
        return self.ref.at[0, 'api_secret']

    def get_gfeed_api_key(self):
        return self.ref.at[0, 'gfeed_api_key']

    def get_gfeed_url(self):
        return self.ref.at[0, 'gfeed_url']


