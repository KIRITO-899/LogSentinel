def parse_windows_event(event):
    """
    Translates a PyWin32 EventLogRecord object directly into the unified JSON format:
    timestamp, hostname, process_name, message, source_ip, severity
    """
    event_id = event.EventID & 0xFFFF
    
    # We care mostly about Application logs and Security logs (auth)
    # 4624 is successful logon, 4625 is failed logon in Security
    log_type = 'syslog'
    if event.SourceName == 'Microsoft-Windows-Security-Auditing':
        log_type = 'auth'
        
    # Map Event log severity
    severity_map = {
        0: 'info', # Success
        1: 'critical', # Error
        2: 'warning', # Warning
        4: 'info', # Information
        8: 'info', # Audit Success
        16: 'critical' # Audit Failure
    }
    severity = severity_map.get(event.EventType, 'info')

    source_ip = None
    message_str = event.SourceName + f" [EventID: {event_id}]"
    
    if getattr(event, "StringInserts", None):
        import re
        ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        for insert in event.StringInserts:
            if insert and isinstance(insert, str):
                ip_match = re.search(ip_regex, insert)
                if ip_match:
                    source_ip = ip_match.group(0)
                    break
        
        if event_id == 4625:
            message_str = "Failed password for invalid user "
            message_str += f"from {source_ip if source_ip else 'unknown'}"
            severity = 'critical'
        elif event_id == 4624:
            message_str = f"Successful logon from {source_ip if source_ip else 'unknown'}"
            
    # Format time
    timestamp = event.TimeGenerated.strftime("%b %d %H:%M:%S")

    return {
        "timestamp": timestamp,
        "hostname": event.ComputerName,
        "process_name": event.SourceName,
        "message": message_str,
        "source_ip": source_ip,
        "severity": severity,
        "log_type": log_type
    }
