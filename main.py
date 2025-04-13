from flask import Flask, request, send_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import io

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

SHEET_NAME = 'Email Tracker'
try:
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    print(f"Error opening sheet: {e}")
    sheet = None

# Store open data in memory (for Open Count & Duration)
open_data = {}

@app.route('/pixel.png')
def pixel():
    email = request.args.get('email', 'Unknown')
    subject = request.args.get('subject', 'No Subject')
    email_subject = f"{email} - {subject}"
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'N/A')
    open_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = datetime.now().strftime('%Y-%m-%d')

    key = email_subject
    if key in open_data:
        prev_time, count = open_data[key]
        duration = (datetime.now() - prev_time).seconds
        count += 1
        open_data[key] = (datetime.now(), count)

        # Update in sheet if already exists
        try:
            cell = sheet.find(email_subject)
            row = cell.row
            sheet.update(f'F{row}', duration)
            sheet.update(f'G{row}', count)
        except:
            # If not found, append as new
            sheet.append_row([timestamp, email_subject, open_time, user_agent, ip, 0, 1])
            open_data[key] = (datetime.now(), 1)
    else:
        # First open
        sheet.append_row([timestamp, email_subject, open_time, user_agent, ip, 0, 1])
        open_data[key] = (datetime.now(), 1)

    # Return 1x1 transparent pixel
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00' \
            b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00' \
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return send_file(io.BytesIO(pixel), mimetype='image/gif')

@app.route('/')
def home():
    return '📩 Email Tracking Server is Running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
