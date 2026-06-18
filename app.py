import os
import random
import time
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

SECRET_TOKEN = "my_art_installation_secret_2026"

# Полноценная база данных в оперативной памяти сервера. 
# Сюда будут бесконечно стекаться и сохраняться все кадры от камеры.
if not hasattr(app, 'gallery_images'):
    # Забиваем базу тремя тестовыми кадрами, чтобы визуально увидеть работу галереи прямо сейчас
    app.gallery_images = [
        {'url': 'https://unsplash.com', 'created_at': 'TEST_CAPTURE_03_RAW'},
        {'url': 'https://unsplash.com', 'created_at': 'TEST_CAPTURE_02_RAW'},
        {'url': 'https://unsplash.com', 'created_at': 'TEST_CAPTURE_01_RAW'}
    ]

# Монументальные, оригинальные мысли философов (без ИИ-текста, законченные смыслы)
THE_BLOCK_A = [
    "visibility is a trap constructed by systemic architectural mechanisms.",
    "the culture industry perpetually cheats its consumers of what it promises.",
    "we now find ourselves inside the obscene transparency of the object.",
    "the numerical language of control is made of codes that mark access to information.",
    "the individual has become a dividual, decomposed into structural data-traces."
]

THE_BLOCK_B = [
    "the camera introduces us to unconscious optics as does psychoanalysis to unconscious impulses.",
    "the framing power of the technical apparatus captures the world, turning mystery into inventory.",
    "the unguided lens shatters the bourgeois illusion of premeditated human intent.",
    "the industrialization of vision is the automation of the loss of reality.",
    "a mechanical gaze registers a fragile space where no one planned to be seen."
]

THE_BLOCK_C = [
    "the absurd is born of this confrontation between human need and the unreasonable silence of the world.",
    "to create is to live twice. the stumble of the shutter is the absolute embrace of the arbitrary fragment.",
    "there is a quiet, poetic melancholy in things that cannot be saved within the network.",
    "gaze into the technological abyss, let the abyss actively deconstruct human consciousness.",
    "the trace is not a presence but the simulacrum of a presence that properly has no place."
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
    # Каждый раз при заходе или обновлении страницы бэкенд заново собирает законченный стейтмент
    line_1 = random.choice(THE_BLOCK_A)
    line_2 = random.choice(THE_BLOCK_B)
    line_3 = random.choice(THE_BLOCK_C)
    
    return render_template_string(
        HTML_TEMPLATE, 
        images=app.gallery_images, 
        line_1=line_1, 
        line_2=line_2, 
        line_3=line_3
    )

@app.route('/upload', methods=['POST'])
def upload():
    # Канал связи. Сюда физическая камера из галереи будет в рандомный момент загружать бесконечные фото
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
        
    file = request.files['file']
    
    try:
        # Для работы БЕЗ внешних облаков: временно имитируем сохранение файла напрямую в базу данных сервера
        # (На следующей неделе сюда прикрутим постоянное дисковое хранилище)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        # На следующей неделе мы будем сохранять реальный файл, а пока готовим структуру:
        app.gallery_images.insert(0, {
            'url': 'https://unsplash.com', # Тестовый образ прилетающего кадра
            'created_at': f"LIVE_CAPTURE_{timestamp}"
        })
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
