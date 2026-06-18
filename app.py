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

# Монументальный массив оригинальных философских тезисов
MANIFESTO_FRAGMENTS = [
    "the automaton becomes the transparent subject, an objective reality through which the mechanism of modern confinement achieves its absolute purification.",
    "power is not held; it is exercised through architectural lattices where visibility functions as an uninterrupted asymmetrical distribution of violence.",
    "the perpetual registry of bodies under a synchronized panoptic apparatus converts the biological interior into a mere function of external visibility.",
    "discourse is not the majestically unfolding manifestation of a thinking subject, but a violent practice imposed upon things.",
    "the radical illusion of the world lies in its non-identity with itself. the image has no relation to any reality whatsoever: it is its own pure simulacrum.",
    "when the real is no longer what it was, nostalgia assumes its full meaning. there is a proliferation of myths of origin and signs of reality.",
    "the ecstasy of communication has replaced the scene of historical meaning. we are now inside the obscene transparency of the object.",
    "the secret is that control does not possess an essence; it is an empty geometric matrix designed to prevent the emergence of a fatal accident.",
    "the absurd is essentially a divorce. it lies in neither of the elements compared; it is born of their confrontation within the silence of the universe.",
    "to create is to live twice. the stumble of the shutter is the rejection of premeditated harmony, an absolute embrace of the arbitrary fragment.",
    "the rebel, by refusing the systematic enclosure of historicist architecture, affirms an immediate proximity with the terrifying freedom of the present.",
    "the absolute absence of a destiny allows the mechanical eye to register the unembellished truth of a fleeting, uncurated cosmos.",
    "enclosures are molds, distinct castings, but controls are a modulation, like a self-deforming cast that will continuously change from one moment to the other.",
    "the numerical language of control is made of codes that mark access to information, or reject it. we no longer find ourselves dealing with the mass/individual pair.",
    "difference is not diversity. diversity is given, but difference is that by which the given is given. the accidental snapshot is the pure manifestation of difference.",
    "the individual has become a 'dividual', decomposed into structural data-traces that circulate through decentralized networks of surveillance.",
    "even the most perfect reproduction of a work of art is lacking in one element: its presence in time and space, its unique existence at the place where it happens to be.",
    "the camera introduces us to unconscious optics as does psychoanalysis to unconscious impulses. the unguided lens shatters the bourgeois illusion of intent.",
    "the destruction of the aura is the signature of a perception whose 'sense of the universal equality of things' has increased to such a degree that it extracts it from a unique object.",
    "the world is a monster of energy, without beginning, without end... a sea of forces flowing and rushing together, eternally changing, eternally flooding back.",
    "there are no moral phenomena at all, but only a moral interpretation of phenomena. the apparatus preserves the raw, pre-interpretive violence of the event.",
    "gazing into the technological abyss does not merely mirror the subject; the abyss actively deconstructs the structural cohesion of human consciousness.",
    "one must still have chaos in oneself to be able to give birth to a dancing star, escaping the mechanical determinism of systemic order.",
    "the trace is not a presence but the simulacrum of a presence that dislocates itself, displacing itself, referring itself, it properly has no place.",
    "there is nothing outside of the text, because the unrecorded space is already inscribed within the overarching violent taxonomy of the system.",
    "hauntology defines the space where the ghost of a non-existent past dictates the impossible architecture of an automated future.",
    "the digital panopticon functions without a central warden. we expose ourselves voluntarily to the field of total visibility, mistaking it for freedom.",
    "transparency is a systemic violence that flattens human existence into data-points, eliminating the sacred shadow of the uninterpretable secret.",
    "the optimization of the self within digital spaces is the ultimate refinement of subjugation, where the worker becomes their own panoptic overseer.",
    "the essence of technology is by no means anything technological. it is a revealing that orders everything into a standing-reserve of calculable assets.",
    "the framing power of the technical apparatus captures the world, turning the sacred mystery of being into an objectified, transparent inventory.",
    "the industrialization of vision is the destruction of the human gaze. the machine sees without perceiving, automating the loss of reality.",
    "the invention of the camera was simultaneously the invention of the accident of the gaze—an immediate catastrophic collision with the unseen.",
    "the culture industry perpetually cheats its consumers of what it perpetually promises. the automated registry is the liquidation of the autonomous ego.",
    "to write poetry after Auschwitz is barbaric, yet to record the raw, mechanical accident of existence is the only remaining refusal of total ideological complicity.",
    "it is easier to imagine the end of the world than the end of capitalism. the systemic enclosure has captured the unconscious itself, leaving only the glitch.",
    "alea iacta est. the radical deployment of a probabilistic interval as an ontological sabotage against deterministic cybernetics.",
    "an archival structure that continuously annihilates its own history in real time, short-circuiting the panoptic urge to accumulate data."
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
        
        sampled = random.sample(MANIFESTO_FRAGMENTS, min(4, len(MANIFESTO_FRAGMENTS)))
        random_statement = " / ".join(sampled)

        return render_template_string(HTML_TEMPLATE, images=images, random_statement=random_statement)
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
