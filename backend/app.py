from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from parsers.syslog_parser import parse_syslog
from parsers.auth_log_parser import parse_auth_log
from analysis.threat_detector import detect_threats

app = Flask(__name__)
CORS(app)

def _get_all_logs():
    logs = []

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(backend_dir, 'data')

    syslog_path = os.path.join(data_dir, 'syslog.log')
    try:
        with open(syslog_path, 'r') as f:
            for line in f:
                parsed_line = parse_syslog(line)
                if parsed_line:
                    parsed_line['log_type'] = 'syslog'
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Warning: {syslog_path} not found.")

    authlog_path = os.path.join(data_dir, 'auth.log')
    try:
        with open(authlog_path, 'r') as f:
            for line in f:
                parsed_line = parse_auth_log(line)
                if parsed_line:
                    parsed_line['log_type'] = 'auth'
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Warning: {authlog_path} not found.")

    return logs


@app.route('/api/logs', methods=['GET', 'POST'])
def logs_api():

    if request.method == 'POST':
        new_log = request.get_json()
        print(new_log)
        return jsonify({"message": "log received"})

    logs = _get_all_logs()
    return jsonify(logs)


@app.route('/api/alerts')
def get_alerts():
    logs = _get_all_logs()
    alerts = detect_threats(logs)
    return jsonify(alerts)


if __name__ == '__main__':
    app.run(debug=True)