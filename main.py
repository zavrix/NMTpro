from flask import Flask, render_template
from monitor import get_status_data
from config import GMAIL_RECEIVER  # Use this instead of RECIPIENT

app = Flask(__name__)

@app.route('/')
def index():
    data = get_status_data()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
