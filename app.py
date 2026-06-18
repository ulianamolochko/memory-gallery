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

# Трехуровневый экзистенциальный монтаж современности
THE_BLOCK_A = [
    "we exist in a state of continuous, fragmented presence.",
    "the interface separates us from the world it promises to show.",
    "wandering through the cold, silent geometry of the digital stream.",
    "our attention is scattered across a thousand flickering screens.",
    "caught in the endless orbit of images that conceal our loneliness."
]

THE_BLOCK_B = [
    "the lens captures a fleeting micro-moment of our fragile reality.",
    "a mechanical gaze registers a space where no one planned to be seen.",
    "the apparatus catches the raw, uncurated optical accident of life.",
    "holding a pixelated reflection of the present directly in volatile memory.",
    "the automated shutter blinks, creating an intimate trace out of nothing."
]

THE_BLOCK_C = [
    "gaze at what the indifference of time has left behind.",
    "an archive that instantly forgets itself, leaving only a ghost of an entry.",
    "there is a quiet, poetic melancholy in things that cannot be saved.",
    "stop trying to organize the chaos. embrace the beautiful glitch of being.",
    "you will close this tab, but this random collision of meanings remains."
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
        .statement-box { max-width: 550px; margin: 0 auto 80px auto; text-align: left; border-left: 1px solid #333; padding-left: 25px; }
        h1 { font-size: 32px; font-weight: normal; letter-spacing: 12px; color: #fff; margin-bottom: 25px; }
        .statement { font-size: 13px; color: #555; text-transform: lowercase; letter-spacing: 1px; line-height: 1.8; }
        .statement p { margin: 0 0 10px 0; }
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
            <p>// {{ line_1 }}</p>
            <p>// {{ line_2 }}</p>
            <p>// {{ line_3 }}</p>
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
        
        # Строим логичное, но случайное стихотворение современности
        line_1 = random.choice(THE_BLOCK_A)
        line_2 = random.choice(THE_BLOCK_B)
        line_3 = random.choice(THE_BLOCK_C)

        return render_template_string(HTML_TEMPLATE, images=images, line_1=line_1, line_2=line_2, line_3=line_3)
    except Exception as e:
        return f"Error: {str(e)}", 500

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
