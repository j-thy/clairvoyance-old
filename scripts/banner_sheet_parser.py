from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from decouple import config
import json
from enum import Enum

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Sources from Officer and Rat's Upcoming Banners Sheet
# https://docs.google.com/spreadsheets/d/1rKtRX3WK9ZpbEHhDTy7yGSxYWIav1Hr_KhNM0jWN2wc
SPREADSHEET_ID = '1rKtRX3WK9ZpbEHhDTy7yGSxYWIav1Hr_KhNM0jWN2wc'

# Google Cloud Credentials (put in .env)
TOKEN_PATH = config('TOKEN_PATH')
CREDS_PATH = config('CREDS_PATH')

# The tabs in the Google Sheet source.
# Data = Banner Data
# Data2 = Servant Data
DATA_SHEETS = ['Data', 'Data2']

# Corresponds to the columns in the banner sheet.
# Example: Fate/Accel Zero | 2018/04/19 | 2018/05/10 | NA | 2
class BannerColumnNum(Enum):
    NAME = 0
    START_DATE = 1
    END_DATE = 2
    REGION = 3
    ID = 4

# Corresponds to the columns in the servant sheet.
# Example: 2 | Perma | Altra Pendragon | [Banner IDs & Solo Rateup]
class ServantColumnNum(Enum):
    ID = 0
    STATUS = 1
    NAME = 2

# Used to serialize the banner data into JSON.
def banner_serializer(obj):
    if isinstance(obj, BannerExport):
        return {
            'jp_name': obj.jp_name,
            'en_name': obj.en_name,
            'jp_wiki_link': obj.jp_wiki_link,
            'en_wiki_link': obj.en_wiki_link,
            'jp_start_date': obj.jp_start_date,
            'en_start_date': obj.en_start_date,
            'jp_end_date': obj.jp_end_date,
            'en_end_date': obj.en_end_date,
            'jp_banner_id': obj.jp_banner_id,
            'en_banner_id': obj.en_banner_id
        }
    return obj.__dict__

# Used to serialize the servant data into JSON.
def servant_serializer(obj):
    if isinstance(obj, ServantExport):
        return {
            'servant_id': obj.servant_id,
            'status': obj.status,
            'name': obj.name,
            'rateups': obj.rateups
        }
    return obj.__dict__

# Format the banner data before serializing it into JSON.
class BannerExport:
    def __init__(self, jp_name, en_name, jp_wiki_link, en_wiki_link, jp_start_date, en_start_date, jp_end_date, en_end_date, jp_banner_id, en_banner_id):
        self.jp_name = jp_name
        self.en_name = en_name
        self.jp_wiki_link = jp_wiki_link
        self.en_wiki_link = en_wiki_link
        self.jp_start_date = jp_start_date
        self.en_start_date = en_start_date
        self.jp_end_date = jp_end_date
        self.en_end_date = en_end_date
        self.jp_banner_id = jp_banner_id
        self.en_banner_id = en_banner_id

# Format the servant data before serializing it into JSON.
class ServantExport:
    def __init__(self, servant_id, status, name, rateups):
        self.servant_id = servant_id
        self.status = status
        self.name = name
        self.rateups = rateups

# Get the banner and servant sheets from the Google Sheet source.
class SheetsData:
    def __init__(self, creds, sheet_id):
        # Call the Sheets API
        service = build('sheets', 'v4', credentials=creds)
        google_sheet = service.spreadsheets()

        # Grab the banner sheet
        self.banner_list = google_sheet.get(
                               spreadsheetId=sheet_id,
                               ranges=DATA_SHEETS[0],
                               includeGridData=True
                           ).execute()

        # Grab the servant sheet
        self.servant_list = google_sheet.get(
                                spreadsheetId=sheet_id,
                                ranges=DATA_SHEETS[1],
                                includeGridData=True
                            ).execute()
    
    # Return the banner sheet rows. Cut out the first row (header).
    def get_banner_list(self):
        return self.banner_list.get('sheets')[0].get('data')[0].get('rowData')[1:]
    
    # Return the servant sheet rows. Cut out the first row (header).
    def get_servant_list(self):
        return self.servant_list.get('sheets')[0].get('data')[0].get('rowData')[1:]

# Get the data from the columns in a banner row.
class BannerRow:
    def __init__(self, row):
        self.row = row
    
    # Get the name of the banner.
    def get_banner_name(self):
        return self.row[BannerColumnNum.NAME.value].get('formattedValue')
    
    # Get the wiki link of the banner.
    def get_banner_link(self):
        return self.row[BannerColumnNum.NAME.value].get('hyperlink')
    
    # Get the start date of the banner.
    def get_banner_start_date(self):
        return self.row[BannerColumnNum.START_DATE.value].get('formattedValue')

    # Get the end date of the banner.
    def get_banner_end_date(self):
        return self.row[BannerColumnNum.END_DATE.value].get('formattedValue')

    # Get the region of the banner.
    def get_banner_region(self):
        return self.row[BannerColumnNum.REGION.value].get('formattedValue')
    
    # Get the banner ID of the banner.
    def get_banner_id(self):
        return self.row[BannerColumnNum.ID.value].get('formattedValue')

# Get the data from the columns in a servant row.
class ServantRow:
    def __init__(self, row):
        self.row = row
        self.num_rateup = len(row) - len(ServantColumnNum)
        # Find the number of rateups in the row.
        for i, column in enumerate(row):
            if 'formattedValue' not in column:
                self.num_rateup = i - len(ServantColumnNum)
                break
            
        
    # Get the servant ID.
    def get_servant_id(self):
        return self.row[0].get('formattedValue')

    # Get the servant status.
    def get_servant_status(self):
        return self.row[1].get('formattedValue')

    # Get the servant name.
    def get_servant_name(self):
        return self.row[2].get('formattedValue')
    
    # Get the rateup banners.
    def get_servant_rateups(self):
        rateup = []
        # For each rateup, add it to the list. (Skip the first 3 columns of the row)
        for i in range(0, self.num_rateup, 2):
            rateup.append(self.row[i + len(ServantColumnNum)].get('formattedValue'))
        return rateup

# Parse the spreadsheet data.
class Spreadsheet:
    def __init__(self, sheet_id, scopes, token_path, creds_path):
        self.banners = {}
        self.servants = {}
        self.sheet_data = SheetsData(self.get_credentials(scopes, token_path, creds_path), sheet_id)
    
    # Get your Google Cloud credentials.
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

    # Create the JSON file for the servant data.
    def create_banner_json(self):
        # Get the rows in the banner sheet.
        banner_list = self.sheet_data.get_banner_list()

        # Read in all the JP banners.
        # (Cut out the buffer rows at the end that have 3 columns instead of 5)
        jp_banners = filter(lambda x: len(x.get('values')) == len(BannerColumnNum) and BannerRow(x.get('values')).get_banner_region() == 'JP', banner_list)
        # Create objects for each JP banner.
        for banner in jp_banners:
            banner_row = BannerRow(banner.get('values'))
            self.banners[banner_row.get_banner_id()] = BannerExport(
                banner_row.get_banner_name(),
                None,
                banner_row.get_banner_link(),
                None,
                banner_row.get_banner_start_date(),
                None,
                banner_row.get_banner_end_date(),
                None,
                banner_row.get_banner_id(),
                None
            )

        # Read in all the NA banners.
        na_banners = filter(lambda x: len(x.get('values')) == len(BannerColumnNum) and BannerRow(x.get('values')).get_banner_region() == 'NA', banner_list)
        # For each NA banner row, check if it has a decimal.
        for banner in na_banners:
            banner_row = BannerRow(banner.get('values'))
            banner_id = banner_row.get_banner_id()
            # If it has .5, check if a JP equivalent exists.
            if banner_id[-2:] == '.5':
                jp_banner_id = banner_id[:-2]
                # If there is a JP banner with the same ID with the .5 removed, add the NA banner's information to the JP banner's object.
                if jp_banner_id in self.banners and self.banners[jp_banner_id].en_banner_id is None:
                    self.banners[jp_banner_id].en_name = banner_row.get_banner_name()
                    self.banners[jp_banner_id].en_wiki_link = banner_row.get_banner_link()
                    self.banners[jp_banner_id].en_start_date = banner_row.get_banner_start_date()
                    self.banners[jp_banner_id].en_end_date = banner_row.get_banner_end_date()
                    self.banners[jp_banner_id].en_banner_id = banner_row.get_banner_id()
                # If there isn't, make a new object for the NA banner.
                else:
                    self.banners[banner_id] = BannerExport(
                        None,
                        banner_row.get_banner_name(),
                        None,
                        banner_row.get_banner_link(),
                        None,
                        banner_row.get_banner_start_date(),
                        None,
                        banner_row.get_banner_end_date(),
                        None,
                        banner_row.get_banner_id()
                    )
            # If it has .6 or doesn't have a decimal, it has no JP equivalent. Make a new object for it.
            else:
                self.banners[banner_id] = BannerExport(
                    None,
                    banner_row.get_banner_name(),
                    None,
                    banner_row.get_banner_link(),
                    None,
                    banner_row.get_banner_start_date(),
                    None,
                    banner_row.get_banner_end_date(),
                    None,
                    banner_row.get_banner_id()
                )

        # Sort the dictionary of banners by their ID.
        self.banners = {k: self.banners[k] for k in sorted(self.banners, key=lambda x: float(x))}
        # Export the banner data to JSON.
        with open('banner_data.json', 'w') as outfile:
            json.dump(self.banners, outfile, default=banner_serializer)
    
    # Create the JSON file for the servant data.
    def create_servant_json(self):
        # Get the rows in the servant sheet.
        servant_list = self.sheet_data.get_servant_list()

        # Create objects for each servant.
        for servant in servant_list:
            # If it reaches the empty rows, break.
            if len(servant) == 0:
                break

            servant_row = ServantRow(servant.get('values'))
            self.servants[servant_row.get_servant_id()] = ServantExport(
                servant_row.get_servant_id(),
                servant_row.get_servant_status(),
                servant_row.get_servant_name(),
                servant_row.get_servant_rateups()
            )

        # Sort the servants by their ID.
        self.servants = {k: self.servants[k] for k in sorted(self.servants, key=lambda x: float(x))}
        # Export the servant data to JSON.
        with open('servant_data.json', 'w') as outfile:
            json.dump(self.servants, outfile, default=servant_serializer)


# Parse the spreadsheet.
banner_servant_sheet = Spreadsheet(SPREADSHEET_ID, SCOPES, TOKEN_PATH, CREDS_PATH)
# Create the JSON file for the banner data.
banner_servant_sheet.create_banner_json()
# Create the JSON file for the servant data.
banner_servant_sheet.create_servant_json()
