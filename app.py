"""Wilson Jarvis API
- POST /command -> store command
- GET /commands -> recent commands
- GET /health -> health check
- GET /config -> client-facing feature flags (no secrets)
- POST /voice -> {message, history?} -> {reply, history}
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, datetime, os, urllib.request

app = Flask(__name__)
CORS(app)

LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'commands.json')

# Wilson's voice personality for the phone call surface.
SYSTEM = ("You are Wilson, Viktor's Hermes personal agent. Reply concisely and "
          "conversationally as if in a voice call: one short paragraph at most, "
          "friendly, opinionated, and actionable. If you do not know something, "
          "say so rather than guessing.")


def _llm(messages, model):
    base = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/") + "/chat/completions"
    key = os.environ.get("LLM_API_KEY", "")
    payload = {"model": model, "messages": messages, "stream": False,
               "max_tokens": 200, "temperature": 0.7}
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(base, data=json.dumps(payload).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/config')
def config():
    return jsonify({
        'voice_enabled': True,
        'provider': 'nous' if os.environ.get('LLM_API_KEY') else 'local-ollama',
        'model': os.environ.get('LLM_MODEL', 'qwen3:8b'),
    })


@app.route('/voice', methods=['POST', 'OPTIONS'])
def voice():
    if request.method == 'OPTIONS':
        return ('', 204)
    body = request.get_json(silent=True) or {}
    message = (body.get('message') or '').strip()
    if not message:
        return jsonify({'error': 'missing message'}), 400
    history = body.get('history') or []
    if not isinstance(history, list):
        history = []
    model = os.environ.get('LLM_MODEL', 'qwen3:8b')
    messages = [{'role': 'system', 'content': SYSTEM}]
    messages += [{'role': h.get('role', 'user'), 'content': str(h.get('content', ''))}
                 for h in history[-6:] if isinstance(h, dict)]
    messages.append({'role': 'user', 'content': message})
    try:
        reply = _llm(messages, model)
    except Exception as exc:
        return jsonify({'error': 'upstream-failure', 'detail': str(exc)}), 502
    out = history + [{'role': 'user', 'content': message},
                     {'role': 'assistant', 'content': reply}]
    return jsonify({'reply': reply, 'history': out})


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
