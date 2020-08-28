import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('HP2020DEMO-a85244012f28.json',scope)
client = gspread.authorize(creds)

spreadSheet = client.open('HP2020LINEBOT')
workSheet = spreadSheet.worksheet('工作表1')

#workSheet.update_cell(1,1,'便當')
#print(workSheet.get_all_values())
workSheet.append_row(['原子筆','滑鼠'])