import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
from pytz import timezone
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def create_creds():
    creds = ServiceAccountCredentials.from_json_keyfile_name("utils/creds.json", SCOPES)
    return creds

def connectSheets():
    creds = create_creds()
    service = gspread.authorize(creds)
    return service

class StorageSheets(object):
    client = connectSheets()

    def __init__(self, sheet_index):
        self.sheet = self.client.open_by_key("1N244Ii_u-68YlA5NiDwO2oKim-LUppo11pSHwuj_Aqs").get_worksheet(sheet_index)

    def add_values(self, values_list: list):
        """Add Values to Spreadsheet

        Args:
            values_list (list): single row of data [id, name, phone_number, email, comment]

        Returns:
            response: response by google api
        """
        tz = timezone("Asia/Kolkata")
        dt = datetime.now(tz=tz)
        date_time = [dt.strftime("%Y/%m/%d"), dt.strftime("%H:%M:%S")]
        values_list.extend(date_time)
        res = self.sheet.insert_row(values_list, index=2)
        return res





