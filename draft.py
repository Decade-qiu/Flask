from PyQt5.QtCore import QUrl
from PyQt5.QtWebSockets import QWebSocket

def onConnected():
    socket.sendTextMessage("Hello, world!")
    print("aa")

def onTextMessageReceived(message):
    print("Message received:", message)

url = QUrl("ws://127.0.0.1:8000/check")
socket = QWebSocket()
socket.open(url)
print(socket.isValid())
socket.connected.connect(onConnected)
socket.sendTextMessage("Hello, world!")
socket.textMessageReceived.connect(onTextMessageReceived)
socket.close()
