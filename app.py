"""
Wilson Jarvis API
- POST /command -> store command
- GET /commands -> recent commands
- GET /health -> health check
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, datetime, os

app = Flask(__name__)
CORS(app)

LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'commands.json')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/command', methods=['POST', 'OPTIONS'])
def command():
    if request.method == 'OPTIONS':
        return ('', 204)
    body = request.get_json(silent=True) or {}
    text = (body.get('command') or '').strip()
    if not text:
        return jsonify({'error': 'empty'}), 400
    entry = {'time': datetime.datetime.now().strftime('%H:%M'), 'command': text}
    data = []
    if os.path.exists(LOG):
        try:
            with open(LOG, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = []
    data.insert(0, entry)
    data = data[:200]
    with open(LOG, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return jsonify({'ok': True})


@app.route('/commands', methods=['GET'])
def commands():
    data = []
    if os.path.exists(LOG):
        try:
            with open(LOG, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = []
    return jsonify(data[:20])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
