from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import sys
import threading
import time

from analysis.threat_detector import detect_threats

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

all_logs = []
all_alerts = []
log_counter = 0

def process_new_log(parsed_line):
    global all_logs, all_alerts, log_counter
    parsed_line['id'] = log_counter
    log_counter += 1
    
    all_logs.append(parsed_line)
    if len(all_logs) > 5000:
        all_logs = all_logs[-5000:]
        
    socketio.emit('new_log', parsed_line)
    
    # Re-evaluate threats
    if parsed_line.get('log_type') == 'auth':
        new_alerts = detect_threats(all_logs)
        if len(new_alerts) > len(all_alerts):
            all_alerts = new_alerts
            socketio.emit('update_alerts', all_alerts)

@app.route('/api/logs', methods=['GET', 'POST'])
def logs_api():
    if request.method == 'POST':
        new_log = request.get_json()
        print(new_log)
        return jsonify({"message": "log received"})
    return jsonify(all_logs)

@app.route('/api/alerts')
def get_alerts():
    return jsonify(all_alerts)

@socketio.on('connect')
def handle_connect():
    socketio.emit('initial_data', {'logs': all_logs, 'alerts': all_alerts})

def start_collectors():
    is_windows = sys.platform == 'win32'
    if is_windows:
        from collectors.windows import collect_windows_logs
        collect_windows_logs(process_new_log, initial_load=True)
        threading.Thread(target=collect_windows_logs, args=(process_new_log, False), daemon=True).start()
    else:
        from collectors.linux import collect_linux_logs
        collect_linux_logs(process_new_log, initial_load=True)
        threading.Thread(target=collect_linux_logs, args=(process_new_log, False), daemon=True).start()

    global all_alerts
    all_alerts = detect_threats(all_logs)

if __name__ == '__main__':
    start_collectors()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)