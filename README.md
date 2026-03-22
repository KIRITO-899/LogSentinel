# 🛡️ LogSentinel: Real-Time Cross-Platform Log Analyzer

**LogSentinel** is a powerful and intuitive web-based dashboard designed to provide a comprehensive, second-by-second overview of your system's security and application events. It natively hooks into your operating system's event pipelines to give you instant visibility into potential threats.

---

## ✨ Key Features

*   **⚡ True Real-Time Ingestion:** Powered by WebSockets (`Flask-SocketIO`), LogSentinel streams events to your browser within milliseconds of them occurring. No database refreshing, no polling delays.
*   **🌍 Cross-Platform Native Agents:** 
    *   **🪟 Windows:** Hooks directly into the `pywin32` Event Log API to capture *Security* and *Application* event streams natively. 
    *   **🐧 Linux:** Recursively tails and parses `/var/log/syslog` and `/var/log/auth.log` files.
*   **🎯 Automated Threat Detection:** Instantly flags security threats—like multiple failed login attempts from a single IP (e.g., Windows Event ID `4625`)—and pushes high-priority alerts straight to the UI.
*   **📊 Dynamic Visualization:** Uses Recharts to render beautiful, live-updating charts showing event velocity over time and distribution across processes.
*   **🔍 Interactive Data Grid:** Explore thousands of logs efficiently with a lightning-fast data grid featuring built-in sorting and filtering.

---

## 🏗️ Architecture

LogSentinel follows a modern, decoupled architecture:

*   **Backend (Python/Flask):** A multi-threaded WebSocket server. On startup, it intelligently detects your host OS (`sys.platform`), spawns a background collector thread to stream native OS events, standardizes the payload into a unified JSON format, and broadcasts it.
*   **Frontend (React):** A responsive Single Page Application (SPA). It establishes a persistent `socket.io-client` connection to ingest the live data stream without ever refreshing the page.

---

## 🚀 Getting Started

Follow these steps to get your LogSentinel dashboard up and running.

### 1. Start the Backend

Open your terminal and navigate to the backend directory. 

> [!IMPORTANT]  
> **Windows Users:** To capture *Security* events (like failed logins), you **must** open your terminal or command prompt as an **Administrator**. Otherwise, only *Application* events will be captured.
> **Linux / WSL Users:** You run perfectly natively inside WSL by tailing the `/var/log/` directory. However, because `/var/log/auth.log` is a protected file, you will need to run the python server with `sudo` privileges.

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS/WSL:
# source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Start the Flask-SocketIO server
# (Windows)
python app.py
# (Linux / WSL - require sudo for auth logs)
# sudo venv/bin/python app.py
```

### 2. Start the Frontend

Open a new terminal window and navigate to the frontend directory:

```bash
cd frontend

# Install React dependencies (including MUI and Socket.io)
npm install

# Start the React development server
npm start
```

### 3. View Your Dashboard
Once both servers are running, open your browser and navigate to:  
🔗 **http://localhost:3000**

You will immediately see your historical system events populate, followed by a live, uninterrupted stream of new activity.

---

## 🛠️ Tech Stack
* **Frontend:** React, Material-UI (DataGrid v8), Recharts, Socket.io-Client
* **Backend:** Python, Flask, Flask-SocketIO, Eventlet, PyWin32 (Windows)

---
*Built with security and speed in mind.*
