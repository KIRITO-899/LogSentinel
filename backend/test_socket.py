import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.on('initial_data')
def on_initial_data(data):
    print(f"Received initial_data: {len(data['logs'])} logs, {len(data['alerts'])} alerts")

@sio.on('new_log')
def on_new_log(data):
    print(f"Received new_log: {data['message']}")

@sio.on('update_alerts')
def on_update_alerts(data):
    print(f"Received update_alerts: {len(data)} alerts now exist")

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()
