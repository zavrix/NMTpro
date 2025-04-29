# main.py

from flask import Flask, render_template, jsonify
from monitor import get_status_data

app = Flask(__name__)

@app.route('/')
def index():
    try:
        data = get_status_data()
    except Exception as e:
        print(f"[ERROR] Failed to get status data: {e}")
        data = {"devices": [], "total": 0, "online": 0, "offline": 0}
    return render_template('dashboard.html', data=data)

@app.route('/status.json')
def status_json():
    try:
        data = get_status_data()
        return jsonify(data)
    except Exception as e:
        print(f"[ERROR] Failed to return status.json: {e}")
        return jsonify({"error": "Failed to fetch status data"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
