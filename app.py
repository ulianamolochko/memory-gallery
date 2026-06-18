import os
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Галерея случайных воспоминаний</title>
    <style>
        body { background-color: #0d0d0d; color: #fff; font-family: monospace; padding: 20px; text-align: center; }
        h1 { font-weight: normal; letter-spacing: 2px; color: #888; margin-top: 40px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; max-width: 1200px; margin: 40px auto; }
        .photo-card { background: #111; padding: 15px; border: 1px solid #222; }
        img { width: 100%; height: auto; filter: grayscale(50%); transition: 0.5s; }
        img:hover { filter: grayscale(0%); }
        .date { font-size: 11px; color: #444; margin-top: 10px; text-align: left; }
    </style>
</head>
<body>
    <h1>СЛУЧАЙНЫЕ СНИМКИ ИНСТАЛЛЯЦИИ</h1>
    <div class="gallery">
        {% for image in images %}
        <div class="photo-card">
            <img src="{{ image.url }}" alt="Воспоминание">
            <div class="date">{{ image.created_at }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

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
