import re

def parse_syslog(line):
    """
    Parses a single line of a syslog message.
    """
    # Example syslog line: "Mar 12 10:30:01 my-laptop CRON[12345]: (root) CMD (command)"
    # A more general regex to handle different syslog formats
    regex = r"(\w+\s+\d+\s+\d{2}:\d{2}:\d{2})\s+([\w\-\.]+)\s+([^:]+):\s+(.*)"
    match = re.match(regex, line)
    if match:
        message = match.group(4).strip()

        # Try to extract an IP address from the message
        ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        ip_match = re.search(ip_regex, message)
        source_ip = ip_match.group(0) if ip_match else None

        # Determine severity level
        lower_message = message.lower()
        if any(keyword in lower_message for keyword in ['fail', 'failed', 'error', 'denied']):
            severity = 'critical'
        elif any(keyword in lower_message for keyword in ['warn', 'warning']):
            severity = 'warning'
        else:
            severity = 'info'

        return {
            "timestamp": match.group(1),
            "hostname": match.group(2),
            "process_name": match.group(3).strip(),
            "message": message,
            "source_ip": source_ip,
            "severity": severity
        }
    return None
