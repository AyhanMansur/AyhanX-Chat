
<div align="center">

# 🤖 AyhanX-Chat

### Real-Time Chat & WebRTC Calling — Deploy Anywhere

A high-performance, Flask-powered communication platform featuring instant messaging, media sharing, and peer-to-peer (P2P) WebRTC calling.

**Designed for speed. Built for connectivity. Ready for the cloud.**

<p align="center"> 
  <img src="https://img.shields.io/badge/Based-Docker-2496ED?logo=docker" /> 
  <img src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway" /> 
</p>

</div>

---

## ✨ Key Features

| Feature | Description |
|---|---|
| ⚡ **Real-Time Messaging** | Instant delivery with an optimized message queue |
| 🎥 **WebRTC Calling** | Seamless P2P audio and video communication |
| 📸 **Media Sharing** | Built-in support for image uploads and file storage |
| 👥 **Presence Tracking** | Real-time monitoring of active users with auto-expiry |
| 🧹 **Auto-Cleanup** | Automatic message rotation to ensure system performance |
| ☁️ **Cloud Ready** | Fully Dockerized and optimized for platforms like Railway |

---

## 🛠️ Technical Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11 · Flask · Gunicorn |
| **Frontend** | HTML5 · CSS3 · JavaScript (WebRTC API) |
| **Concurrency** | Threading (auto-cleanup & background tasks) |
| **Deployment** | Docker · Railway |

</div>

---

## 📁 Project Structure

```
AyhanX-Chat/
├── app.py                  # Main Flask application logic
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment instructions for Railway
├── static/
│   └── uploads/            # User-uploaded media
└── templates/
    └── index.html          # Main chat application UI
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.11+**
- Docker *(if deploying via container)*

### 🖥️ Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/AyhanMansur/AyhanX-Chat.git
cd AyhanX-Chat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open in your browser
# https://127.0.0.1:5000
```

> ⚠️ **Note:** You must accept the SSL security warning — the app uses a local self-signed certificate for development.

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t ayhanx-chat .

# Run the container
docker run -p 5000:5000 ayhanx-chat
```

---

## ⚙️ Configuration

| Setting | Value |
|---|---|
| **Port** | Hardcoded to `5000` |
| **Storage** | Uploaded files → `static/uploads/` |
| **Signaling** | In-memory `message_queue` — offers, answers, and ICE candidates are stored temporarily and cleared upon retrieval for low-latency P2P handshakes |

---

## 📝 Important Notes

> **🔒 Security**
> The app uses `ssl_context='adhoc'` for local development. When deploying to production (e.g., Railway), the platform provides valid SSL/HTTPS — **mandatory** for accessing camera/microphone hardware.

> **🌐 WebRTC Connectivity**
> If testing across different networks (mobile data vs. Wi-Fi), add STUN servers to your `RTCPeerConnection` config:
> ```javascript
> const rtcConfig = {
>   iceServers: [{ urls: 'stun:stun1.l.google.com:19302' }]
> };
> ```

> **💾 Data Persistence**
> Messages and users are stored in memory. Server restarts or container redeployments will clear chat history and the online user list.

---

## 🌐 Deploy to Railway
<p align="center"> 
  <img src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway" /> 
</p>

<div align="center">

## 👨‍💻 Developed By

**Ayhan Mansur**

![GitHub](https://img.shields.io/badge/GitHub-AyhanMansur-181717?style=for-the-badge&logo=github&logoColor=white)

⭐ **If you find this project useful, give it a star!** ⭐

</div>
