from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# 处理客户端发送的音频数据
@socketio.on('audio_data')
def handle_audio_data(audio_data):
  # 广播音频数据给所有其他客户端
  emit('audio_data', audio_data, broadcast=True)

if __name__ == '__main__':
  socketio.run(app)