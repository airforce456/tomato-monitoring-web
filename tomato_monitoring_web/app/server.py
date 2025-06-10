from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('0.0.0.0', 5005))  # Jetson端通过UDP发送数据到此端口
    while True:
        data, _ = udp_sock.recvfrom(1024)
        try:
            message = data.decode('utf-8')
            socketio.emit('tomato_data', message)
        except Exception as e:
            print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=10000)