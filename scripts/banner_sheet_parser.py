from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from decouple import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
BANNER_SPREADSHEET_ID = '1rKtRX3WK9ZpbEHhDTy7yGSxYWIav1Hr_KhNM0jWN2wc'
TOKEN_PATH = config('TOKEN_PATH')
CREDS_PATH = config('CREDS_PATH')
DATA_SHEETS = ['Data', 'Data2']

class Banner:
    def __init__(self, jp_banner_id, en_banner_id, jp_name, en_name, jp_wiki_link, en_wiki_link, jp_start_date, en_start_date):
        self.jp_banner_id = jp_banner_id
        self.en_banner_id = en_banner_id
        self.jp_name = jp_name
        self.en_name = en_name
        self.jp_wiki_link = jp_wiki_link
        self.en_wiki_link = en_wiki_link
        self.jp_start_date = jp_start_date
        self.en_start_date = en_start_date

class Servant:
    def __init__(self, servant_id):
        self.servant_id = servant_id
        self.rateup = {}

class BannerData:
    def __init__(self, creds, sheet_id):
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        google_sheet = service.spreadsheets()

        # Parse each class' banner sheet
        self.banner_list = google_sheet.get(
                               spreadsheetId=sheet_id,
                               ranges=DATA_SHEETS[0],
                               includeGridData=True
                           ).execute()

        self.servant_list = google_sheet.get(
                                spreadsheetId=sheet_id,
                                ranges=DATA_SHEETS[1],
                                includeGridData=True
                            ).execute()
    
    def get_banner_list(self):
        return self.banner_list.get('sheets')[0].get('data')[0].get('rowData')[1:]
    
    def get_servant_list(self):
        return self.servant_list.get('sheets')[0].get('data')[0].get('rowData')[1:]


class BannerSpreadsheet:
    def __init__(self, sheet_id, scopes, token_path, creds_path):
        self.sheet_id = sheet_id
        self.creds = self.get_credentials(scopes, token_path, creds_path)
        self.banners = {}
        self.servants = []
    
    def get_credentials(self, scopes, token_path, creds_path):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def create_banner_json(self, sheet_ranges_list):
        banner_data = BannerData(self.creds, self.sheet_id)

        banner_list = banner_data.get_banner_list()

        jp_banners = filter(lambda x: x.get('values')[3].get('formattedValue').strip() == 'JP', banner_list)
        en_banners = filter(lambda x: x.get('values')[3].get('formattedValue').strip() == 'NA', banner_list)

        for banner in jp_banners:
            banner_values = banner.get('values')
            jp_name = 
            print('test')


        servant_list = banner_data.get_servant_list()

        print('testing')

banner_sheet = BannerSpreadsheet(BANNER_SPREADSHEET_ID, SCOPES, TOKEN_PATH, CREDS_PATH)
banner_sheet.create_banner_json(DATA_SHEETS)