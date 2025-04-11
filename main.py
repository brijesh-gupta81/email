from flask import Flask, Response, request
import datetime
import logging
import base64

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename="tracker.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Base64 encoded 1x1 transparent PNG
PIXEL_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
    "ASsJTYQAAAAASUVORK5CYII="
)

@app.route('/')
def home():
    return '<h2>Email Tracker is Running ✅</h2>'

@app.route('/pixel')
def pixel():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log hit
    logging.info(f"Pixel Hit | IP: {ip} | Time: {time} | User-Agent: {user_agent}")

    # Serve 1x1 pixel image
    pixel_data = base64.b64decode(PIXEL_BASE64)
    return Response(pixel_data, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
