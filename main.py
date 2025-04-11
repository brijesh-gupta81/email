import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request
from datetime import datetime
import user_agents

app = Flask(__name__)

# Google Sheet Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sonam").sheet1

# Store open timestamps to calculate duration
open_times = {}

@app.route("/tracker.png")
def tracker():
    ip = request.remote_addr
    user_agent_str = request.headers.get('User-Agent')
    ua = user_agents.parse(user_agent_str)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if ip not in open_times:
        open_times[ip] = time.time()
        duration = 0
    else:
        duration = round(time.time() - open_times[ip], 2)  # in seconds

    sheet.append_row([
        ts,
        ip,
        ua.browser.family + " " + ua.browser.version_string,
        ua.os.family + " " + ua.os.version_string,
        ua.device.family,
        str(duration) + " sec"
    ])

    # Send a 1x1 transparent pixel
    from flask import send_file
    from io import BytesIO
    pixel = BytesIO(b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b")
    return send_file(pixel, mimetype='image/gif')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
