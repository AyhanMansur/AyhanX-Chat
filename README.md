
# 💬 Real-Time Chat & WebRTC Calling

A high-performance, Flask-powered communication platform featuring instant messaging, media sharing, and peer-to-peer (P2P) WebRTC calling capabilities. Designed for speed, ease of use, and seamless real-time connectivity.

## 🚀 Key Features

*   **⚡ Real-Time Messaging:** Instant delivery with an optimized message queue.
*   **📞 WebRTC Calling:** Seamless P2P audio and video communication.
*   **🖼️ Media Sharing:** Built-in support for image uploads and file storage.
*   **👤 Presence Tracking:** Real-time monitoring of active users with auto-expiry.
*   **🧹 Auto-Cleanup:** Automatic message rotation to ensure system performance.
*   **☁️ Cloud Ready:** Fully Dockerized and optimized for platforms like Railway.

---

## 🛠 Technical Stack

*   **Backend:** Python 3.11, Flask, Gunicorn
*   **Frontend:** HTML5, CSS3, JavaScript (WebRTC API)
*   **Concurrency:** Threading (for auto-cleanup and background tasks)
*   **Deployment:** Docker, Railway

---

## 📂 Project Structure

```text
├── app.py              # Main Flask application logic
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment instructions for Railway
├── static/             # Assets and uploads
│   └── uploads/        # User-uploaded media
└── templates/          # HTML interfaces
    └── index.html      # Main chat application UI

```

---

## Getting Started

### Prerequisites

* Python 3.11+
* Docker (if deploying via container)

### Local Setup

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
cd your-repo-name

```


2. Install dependencies:
```bash
pip install -r requirements.txt

```


3. Run the application:
```bash
python app.py

```


4. Visit https://127.0.0.1:5000 in your browser. Note: You must accept the SSL security warning as the app uses a local self-signed certificate for development.

---

## Docker Deployment

To build and run the project using Docker:

```bash
# Build the image
docker build -t chat-app .

# Run the container
docker run -p 5000:5000 chat-app

```

---

## Project Configuration

* **Port:** The application is hardcoded to port 5000.
* **Storage:** Uploaded files are stored in `static/uploads/`.
* **Signaling:** The app uses an in-memory `message_queue`. Signals (offers, answers, ICE candidates) are stored temporarily and cleared upon retrieval to maintain low-latency P2P handshakes.

---

## Important Notes

* **Security:** This app uses `ssl_context='adhoc'` for local development. When deploying to production (like Railway), the platform will provide valid SSL/HTTPS, which is mandatory for accessing camera/microphone hardware.
* **WebRTC Connectivity:** If testing across different networks (e.g., mobile data vs. Wi-Fi), ensure you update your `RTCPeerConnection` configuration to include STUN servers:
```javascript
const rtcConfig = {
    iceServers: [{ urls: 'stun:stun1.l.google.com:19302' }]
};

```


* **Data Persistence:** The application uses in-memory storage for messages and users. Server restarts or container redeployments will clear the current chat history and online user list.

---
## Developed By **Ayhan Mansur**
