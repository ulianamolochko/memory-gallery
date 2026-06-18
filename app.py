import os
import random
from flask import Flask, request, render_template_string, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# Настройки связи с твоим облаком Cloudinary
cloudinary.config(
  cloud_name = "dkk8iqf6p",
  api_key = "946533445816386",
  api_secret = "utBQxo1xonoZiY1E9zI_I6e-Bvk",
  secure = True
)

SECRET_TOKEN = "my_art_installation_secret_2026"

# Элементы концепта, которые сайт будет хаотично перемешивать при каждом обновлении
MANIFESTO_FRAGMENTS = [
    "control is a simulation.",
    "the eye without memory.",
    "panopticon deconstruction.",
    "surrender to chaos.",
    "absurdity of order.",
    "what the void has chosen.",
    "erasing memories in real time."
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALEA</title>
    <style>
        body { background-color: #030303; color: #a3a3a3; font-family: monospace; padding: 60px 20px; text-align: center; }
        .statement-box { max-width: 500px; margin: 0 auto 80px auto; text-align: left; border-left: 1px solid #222; padding-left: 20px; }
        h1 { font-size: 32px; font-weight: normal; letter-spacing: 12px; color: #fff; margin-bottom: 25px; }
        .statement { font-size: 12px; color: #555; text-transform: lowercase; letter-spacing: 1px; line-height: 1.8; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .photo-card { background: #000; padding: 10px; border: 1px solid #111; }
        img { width: 100%; height: auto; filter: grayscale(100%) contrast(120%); transition: 0.5s ease; }
        img:hover { filter: grayscale(0%) contrast(100%); }
        .date { font-size: 9px; color: #222; margin-top: 10px; text-align: right; }
    </style>
</head>
<body>
    <div class="statement-box">
        <h1>ALEA</h1>
        <div class="statement">
            // {{ random_statement }}
        </div>
    </div>
    <div class="gallery">
        {% for image in images %}
        <div class="photo-card">
            <img src="{{ image.url }}" alt="alea snapshot">
            <div class="date">{{ image.created_at }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>

@app.route('/')
def index():
    try:
        resources = cloudinary.api.resources(type="upload", prefix="installation", max_results=100)
        images = []
        sorted_resources = sorted(resources.get('resources', []), key=lambda x: x['created_at'], reverse=True)
        for res in sorted_resources:
            images.append({
                'url': res['secure_url'],
                'created_at': res['created_at'].replace('T', ' ').replace('Z', '')
            })
        return render_template_string(HTML_TEMPLATE, images=images)
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

@app.route('/upload', methods=['POST'])
def upload():
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    try:
        upload_result = cloudinary.uploader.upload(file, folder="installation")
        return jsonify({"status": "success", "url": upload_result['secure_url']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
