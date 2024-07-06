from flask import Flask, request, jsonify
import requests
import base64
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://verbovisions.web.app"}})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)