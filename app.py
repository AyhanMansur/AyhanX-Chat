from flask import Flask, render_template, request, jsonify, send_from_directory
import uuid
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Note: In production on Railway, these are in-memory and will reset 
# if the container restarts.
messages = []
active_users = {}

def auto_delete_old_messages():
    while True:
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=5)
        global messages
        messages = [m for m in messages if datetime.fromisoformat(m['timestamp']) > cutoff]
        time.sleep(60)

thread = threading.Thread(target=auto_delete_old_messages, daemon=True)
thread.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username', '').strip()
    if username and username not in active_users:
        active_users[username] = datetime.utcnow().isoformat()
        return jsonify({'status': 'success', 'users': list(active_users.keys())})
    return jsonify({'status': 'error'}), 400

@app.route('/get_users', methods=['GET'])
def get_users():
    now = datetime.utcnow()
    # Remove users inactive for more than 60 seconds
    inactive = [u for u, ts in active_users.items() if (now - datetime.fromisoformat(ts)).total_seconds() > 60]
    for u in inactive:
        del active_users[u]
    return jsonify(list(active_users.keys()))

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    username = data.get('username', 'Anonymous')
    text = data.get('text', '').strip()
    msg_type = data.get('type', 'text')
    media_url = data.get('media_url', '')

    if username in active_users:
        active_users[username] = datetime.utcnow().isoformat()

    msg = {
        'id': str(uuid.uuid4()),
        'username': username,
        'text': text,
        'type': msg_type,
        'media_url': media_url,
        'timestamp': datetime.utcnow().isoformat()
    }
    messages.append(msg)
    if len(messages) > 500:
        messages[:] = messages[-500:]
    return jsonify({'status': 'success'}), 200

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error'}), 400

    ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
    new_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    file.save(save_path)
    return jsonify({'status': 'success', 'url': f"/static/uploads/{new_name}"})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Railway handles port automatically
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
