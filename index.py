from flask import Flask, request, jsonify, make_response
import pyperclip

app = Flask(__name__)

def cors(resp):
    # If you want to lock it down, replace * with your GitHub Pages origin.
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, ngrok-skip-browser-warning"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return resp

@app.before_request
def log_req():
    print(">>>", request.method, request.path)

@app.route("/copy", methods=["POST", "OPTIONS"])
def copy():
    if request.method == "OPTIONS":
        return cors(make_response("", 204))

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return cors(jsonify({"ok": False, "error": "empty"})), 400

    pyperclip.copy(text)
    return cors(jsonify({"ok": True})), 200

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
