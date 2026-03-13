from collections import defaultdict

def detect_threats(logs):
    """
    Analyzes log data to detect potential threats.
    """
    alerts = []
    failed_logins = defaultdict(int)

    for log in logs:
        if log.get('log_type') == 'auth' and 'failed password' in log.get('message', '').lower():
            # Extract IP address from the message
            # Example message: "Failed password for invalid user guest from 192.168.1.100 port 22 ssh2"
            parts = log['message'].split(' ')
            try:
                ip_index = parts.index('from') + 1
                ip_address = parts[ip_index]
                failed_logins[ip_address] += 1
            except (ValueError, IndexError):
                pass # Could not extract IP

    for ip, count in failed_logins.items():
        if count >= 3:
            alerts.append({
                "type": "Multiple Failed Logins",
                "message": f"{count} failed login attempts from IP address {ip}",
                "ip_address": ip
            })

    return alerts
