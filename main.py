from flask import Flask, send_file, request
from datetime import datetime
import os

app = Flask(__name__)

# Ensure logs.txt exists
if not os.path.exists("logs.txt"):
    with open("logs.txt", "w") as f:
        f.write("=== Email Open Logs ===\n")

@app.route("/")
def home():
    return "📬 Email Tracker is Live!"

@app.route("/track/<email_id>")
def track_email(email_id):
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{time} | {email_id} opened | IP: {ip} | UA: {user_agent}\n"
    
    with open("logs.txt", "a") as f:
        f.write(log_entry)

    return send_file("static/pixel.png", mimetype="image/png")

@app.route("/logs")
def view_logs():
    with open("logs.txt", "r") as f:
        return "<pre>" + f.read() + "</pre>"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
