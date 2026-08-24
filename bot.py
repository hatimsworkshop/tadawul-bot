
import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials
import yfinance as yf

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
gc = gspread.authorize(creds)

sheet_name = "سجل محفظة التداول الافتراضية - السوق السعودي (V2)"
sh = gc.open(sheet_name)
worksheet = sh.get_worksheet(0)

watchlist = [
    {"symbol": "2220.SR", "name": "2220 - أرامكو السعودية"},
    {"symbol": "2010.SR", "name": "2010 - سابك"},
    {"symbol": "1180.SR", "name": "1180 - مصرف الإنماء"},
    {"symbol": "7010.SR", "name": "7010 - اس تي سي (STC)"},
    {"symbol": "1211.SR", "name": "1211 - معادن"},
    {"symbol": "4200.SR", "name": "4200 - شركة الدريس"}
]

day_of_year = datetime.datetime.now().timetuple().tm_yday
selected_stock = watchlist[day_of_year % len(watchlist)]

ticker = yf.Ticker(selected_stock["symbol"])
df = ticker.history(period="2d")
if not df.empty:
    real_price = float(df['Close'].iloc[-1])
else:
    real_price = 30.0

current_date = str(datetime.date.today())
starting_capital = 100000.0
allocated_amount = 20000.0

shares_count = int(allocated_amount / real_price)
total_cost = shares_count * real_price
remaining_cash = starting_capital - total_cost

row_data = [
    current_date,
    selected_stock["name"],
    "شراء آلي (مجدول أوتوماتيك)",
    shares_count,
    round(real_price, 2),
    round(total_cost, 2),
    round(remaining_cash, 2),
    "نشطة في المحفظة",
    f"تشغيل آلي من GitHub | السعر: {real_price} | الكاش المتبقي: {remaining_cash:,.2f}"
]

worksheet.append_row(row_data)
print("تمت عملية التحديث الآلي لملف الإكسل بنجاح!")
