from flask import Flask, render_template, request, jsonify, send_from_directory
import uuid
import os
from datetime import datetime, timedelta
import threading
import time
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
messages = []
active_users = {}
def auto_delete_old_messages():
    while True:
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=5)
        global messages
        before = len(messages)
        messages = [m for m in messages if datetime.fromisoformat(m['timestamp']) > cutoff]
        if len(messages) != before:
            print(f"🧹 Auto-delete: removed {before - len(messages)} old messages")
        time.sleep(30)

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
        print(f"✅ User registered: {username}")
        return jsonify({'status': 'success', 'users': list(active_users.keys())})
    return jsonify({'status': 'error'}), 400

@app.route('/get_users', methods=['GET'])
def get_users():
    now = datetime.utcnow()
    inactive = [u for u, ts in active_users.items() if (now - datetime.fromisoformat(ts)).total_seconds() > 60]
    for u in inactive:
        print(f"🚪 User inactive: {u}")
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
    print(f"📩 New message: {msg_type} from {username} (target: {data.get('target', 'none')})")

    return jsonify({'status': 'success'}), 200

@app.route('/get_messages', methods=['GET'])
def get_messages():
    print(f"📨 GET /get_messages -> returning {len(messages)} messages")
    return jsonify(messages)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'msg': 'No file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'msg': 'No file selected'}), 400

    ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
    new_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    file.save(save_path)
    url = f"/static/uploads/{new_name}"
    return jsonify({'status': 'success', 'url': url})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_message', methods=['POST'])
def delete_message():
    data = request.json
    message_id = data.get('id')
    username = data.get('username')
    if not message_id or not username:
        return jsonify({'status': 'error'}), 400

    for i, msg in enumerate(messages):
        if msg.get('id') == message_id:
            if msg.get('username') != username:
                return jsonify({'status': 'error', 'msg': 'Not your message'}), 403
            messages.pop(i)
            delete_signal = {
                'id': str(uuid.uuid4()),
                'username': 'system',
                'text': message_id,
                'type': 'delete',
                'timestamp': datetime.utcnow().isoformat()
            }
            messages.append(delete_signal)
            if len(messages) > 500:
                messages[:] = messages[-500:]
            print(f"🗑️  Deleted message {message_id} by {username}")
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'msg': 'Message not found'}), 404

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("\n" + "="*50)
    print("💬 WhatsApp-like Chat (HTTPS) – with logging")
    print(f"📍 https://127.0.0.1:5000")
    print(f"📍 https://{local_ip}:5000")
    print("📌 Accept the certificate warning in your browser.")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')