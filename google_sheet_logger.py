import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheets(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def log_trade(sheet, row_data):
    trade_log = sheet.worksheet("Trade Log")
    trade_log.append_row(row_data)

def update_summary(sheet, total_trades, accuracy):
    summary = sheet.worksheet("Summary")
    summary.update("A2", [["Total Trades", total_trades],
                          ["ML Accuracy", f"{accuracy:.2%}"]])
