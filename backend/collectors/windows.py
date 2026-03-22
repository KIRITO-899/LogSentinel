import time

def collect_windows_logs(callback, initial_load=False):
    try:
        import win32evtlog
    except ImportError:
        print("pywin32 not available")
        return

    server = 'localhost'
    
    hand_sec = None
    try:
        hand_sec = win32evtlog.OpenEventLog(server, 'Security')
    except Exception as e:
        print("Warning: Requires Administrator to read Security Event Log:", e)

    hand_app = None
    try:
        hand_app = win32evtlog.OpenEventLog(server, 'Application')
    except Exception as e:
        print("Error accessing Application Event Log:", e)
        
    if not hand_sec and not hand_app:
        return

    from parsers.windows_parser import parse_windows_event

    def fetch_recent(hand, count=50):
        records = []
        try:
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                records.extend(events[:count])
        except Exception:
            pass
        return records

    if initial_load:
        sec_events = fetch_recent(hand_sec, 50)
        app_events = fetch_recent(hand_app, 50)
        all_evs = sec_events + app_events
        all_evs.sort(key=lambda x: x.TimeGenerated)
        for ev in all_evs:
            parsed = parse_windows_event(ev)
            if parsed:
                callback(parsed)
        return

    # Tailing logic
    def get_latest_record(hand):
        try:
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                return events[0].RecordNumber
        except:
            return 0
        return 0

    next_sec = get_latest_record(hand_sec) + 1
    next_app = get_latest_record(hand_app) + 1

    while True:
        try:
            flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEEK_READ
            # Poll security
            try:
                sec_events = win32evtlog.ReadEventLog(hand_sec, flags, next_sec)
                if sec_events:
                    for ev in sec_events:
                        parsed = parse_windows_event(ev)
                        if parsed: callback(parsed)
                        next_sec = ev.RecordNumber + 1
            except Exception:
                pass
            
            # Poll application
            try:
                app_events = win32evtlog.ReadEventLog(hand_app, flags, next_app)
                if app_events:
                    for ev in app_events:
                        parsed = parse_windows_event(ev)
                        if parsed: callback(parsed)
                        next_app = ev.RecordNumber + 1
            except Exception:
                pass

            time.sleep(1)
        except Exception as e:
            time.sleep(1)
