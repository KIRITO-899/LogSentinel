import os
import time

def collect_linux_logs(callback, initial_load=False):
    from parsers.syslog_parser import parse_syslog
    from parsers.auth_log_parser import parse_auth_log
    
    syslog_path = '/var/log/syslog'
    authlog_path = '/var/log/auth.log'

    if initial_load:
        def get_last_lines(path, count=50):
            if not os.path.exists(path): return []
            try:
                with open(path, 'r') as f:
                    return f.readlines()[-count:]
            except PermissionError:
                print(f"Permission denied reading {path}")
                return []
        
        syslogs = get_last_lines(syslog_path)
        for line in syslogs:
            parsed = parse_syslog(line)
            if parsed:
                parsed['log_type'] = 'syslog'
                callback(parsed)

        authlogs = get_last_lines(authlog_path)
        for line in authlogs:
            parsed = parse_auth_log(line)
            if parsed:
                parsed['log_type'] = 'auth'
                callback(parsed)
        return

    syslog_f = open(syslog_path, 'r') if os.path.exists(syslog_path) else None
    authlog_f = open(authlog_path, 'r') if os.path.exists(authlog_path) else None

    if syslog_f: syslog_f.seek(0, 2)
    if authlog_f: authlog_f.seek(0, 2)

    while True:
        updated = False
        if syslog_f:
            line = syslog_f.readline()
            if line:
                parsed = parse_syslog(line)
                if parsed:
                    parsed['log_type'] = 'syslog'
                    callback(parsed)
                updated = True
        
        if authlog_f:
            line = authlog_f.readline()
            if line:
                parsed = parse_auth_log(line)
                if parsed:
                    parsed['log_type'] = 'auth'
                    callback(parsed)
                updated = True
                
        if not updated:
            time.sleep(0.5)
