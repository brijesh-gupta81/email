from flask import Flask, request, send_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Your sheet name
SHEET_NAME = 'Email Tracker'

try:
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    print(f"Error opening sheet: {e}")
    sheet = None

@app.route('/pixel.png')
def pixel():
    email = request.args.get('email')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log to Google Sheet
    if sheet and email:
        sheet.append_row([email, ip, user_agent, timestamp])
        print(f"Logged: {email}, {ip}, {timestamp}")
    else:
        print("Missing email or Google Sheet not connected")

    return send_file('static/pixel.png', mimetype='image/png')

@app.route('/')
def home():
    return 'Email tracking pixel server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
