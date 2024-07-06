from flask import Flask, request, jsonify, send_file
import os
import requests
import base64
from PIL import Image
import io
from flask_cors import CORS
import time
from threading import Timer
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://verbovisions.web.app"}})

if not os.path.exists("images"):
    os.makedirs("images")

def delete_image(image_path):
    time.sleep(120)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Server is alive"})

@app.route('/generate', methods=['GET'])
def generate_image():
    user_prompt = request.args.get('p')
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://magicstudio.com",
        "Referer": "https://magicstudio.com/ai-art-generator/",
    }

    data = {
        "prompt": user_prompt,
        "output_format": "bytes",
        "user_profile_id": "null",
        "anonymous_user_id": "a584e30d-1996-4598-909f-70c7ac715dc1",
        "request_timestamp": "1715704441.446",
        "user_is_subscribed": "false",
        "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return jsonify({"img": img_str})
    else:
        return jsonify({"error": "Failed to fetch image", "status_code": response.status_code}), response.status_code

# ======= PREMIUM USERS =======
@app.route('/image', methods=['GET'])
def make_image():
    prompt = request.args.get('p')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://magicstudio.com",
        "Referer": "https://magicstudio.com/ai-art-generator/",
    }

    data = {
        "prompt": prompt,
        "output_format": "bytes",
        "user_profile_id": "null",
        "anonymous_user_id": "c75c20fe-57af-4d71-86fd-754b82b4bf54",
        "request_timestamp": str(time.time()),
        "user_is_subscribed": "false",
        "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            image_path = f"images/{timestamp}.png"
            image.save(image_path)
            Timer(120, delete_image, [image_path]).start()
            return jsonify({"url": f"/images/{timestamp}.png"})
        else:
            return jsonify({"error": "Failed to fetch image. Status code: " + str(response.status_code)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_file(os.path.join("images", filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
