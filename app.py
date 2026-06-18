import os
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALEA</title>
    <style>
        body { background-color: #030303; color: #a3a3a3; font-family: monospace; padding: 60px 20px; text-align: center; }
        .statement-box { max-width: 600px; margin: 0 auto 80px auto; text-align: left; border-left: 1px solid #333; padding-left: 25px; }
        h1 { font-size: 32px; font-weight: normal; letter-spacing: 12px; color: #fff; margin-bottom: 25px; }
        .statement { font-size: 13px; color: #666; letter-spacing: 1px; line-height: 1.8; text-align: left; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .photo-card { background: #080808; padding: 40px 20px; border: 1px dashed #222; min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .date { font-size: 9px; color: #333; margin-top: 15px; }
        button { background: none; border: 1px solid #222; color: #444; font-family: monospace; padding: 8px 15px; margin-top: 30px; cursor: pointer; font-size: 11px; }
        button:hover { color: #888; border-color: #444; }
    </style>
</head>
<body>
    <div class="statement-box">
        <h1>ALEA</h1>
        <div class="statement" id="manifesto">
            <!-- Высказывание вставится через JavaScript -->
        </div>
        <button onclick="generateStatement()">// re-examine reality</button>
    </div>
    
    <div class="gallery">
        <div class="photo-card">
            <div style="color: #888; font-size: 12px; font-weight: bold; letter-spacing: 1px;">[CAMERA_DISCONNECTED]</div>
            <div class="date">SYSTEM_OFFLINE</div>
        </div>
        <div class="photo-card">
            <div style="color: #888; font-size: 12px; font-weight: bold; letter-spacing: 1px;">[WAITING_FOR_THE_ACCIDENT]</div>
            <div class="date">PROBABILITY_CYCLE</div>
        </div>
        <div class="photo-card">
            <div style="color: #888; font-size: 12px; font-weight: bold; letter-spacing: 1px;">[MEMORY_NOT_FOUND]</div>
            <div class="date">RAM_EMPTY</div>
        </div>
    </div>

    <script>
        // Сформированные, целостные кураторские высказывания на основе оригинальной философии
        const statementsPool = [
            "we exist inside the obscene transparency of the digital object, where the interface systematically separates us from the world it promises to show. substitution of signs of the real for the real creates an endless orbit of images designed to mask the terrifying absence of historical meaning.",
            "visibility functions as an uninterrupted asymmetrical distribution of violence. he who is subjected to a field of visibility assumes internal responsibility for the constraints of modern confinement, while the numerical language of decentralized control marks access through continuous modulations.",
            "the unguided lens shatters the bourgeois illusion of premeditated human intent, introducing us to an industrialization of vision where the machine sees without perceiving. this framing power captures the world, turning the sacred mystery of being into an objectified, transparent inventory.",
            "to record the raw, mechanical accident of existence is the only remaining refusal of total ideological complicity. the stumble of the automated shutter is a radical rejection of premeditated harmony, an absolute embrace of the arbitrary fragment within a volatile system.",
            "the absurd is born of this direct confrontation between the human need for order and the unreasonable silence of a world flowing with monstrous energy. creating an archive that instantly forgets itself becomes the ultimate destruction of systemic tyranny and historicist enclosure."
        ];

        function generateStatement() {
            // Выбираем одно монолитное высказывание
            const randomStatement = statementsPool[Math.floor(Math.random() * statementsPool.length)];
            document.getElementById('manifesto').innerHTML = '// ' + randomStatement;
        }

        // Автоматический старт первого высказывания при загрузке
        generateStatement();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    return jsonify({"status": "ready_for_hardware"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
