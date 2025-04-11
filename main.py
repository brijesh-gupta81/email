from flask import Flask, request
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from user_agents import parse as parse_user_agent

app = Flask(__name__)

# 1. Create credentials.json from ENV
if not os.path.exists("credentials.json"):
    creds_data = os.environ.get("GOOGLE_CREDS")
    if creds_data:
        with open("credentials.json", "w") as f:
            f.write(creds_data)
    else:
        raise Exception("GOOGLE_CREDS env variable is missing!")

# 2. Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 3. Open your sheet
spreadsheet = client.open("Sonam")  # 👈 change this
worksheet = spreadsheet.sheet1

@app.route('/')
def home():
    return "✅ Email Tracker is running!"

@app.route('/track', methods=['GET'])
def track():
    # 4. Get IP and User Agent
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    ua = parse_user_agent(user_agent)

    device_info = f"{ua.device.family}, {ua.os.family} {ua.os.version_string}, {ua.browser.family} {ua.browser.version_string}"

    # 5. Log to sheet
    worksheet.append_row([user_ip, device_info])

    # 6. Return a tiny transparent pixel (tracker image)
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00' \
            b'\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00' \
            b'\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B'
    return pixel, 200, {'Content-Type': 'image/gif'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
