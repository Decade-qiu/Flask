import json
import datetime
from sockjs.tornado import SockJSConnection
from model.CRUD import CRUD


class CanvasConnection(SockJSConnection):
    clients = set()

    def on_open(self, info):
        self.clients.add(self)

    def on_message(self, message):
        for client in self.clients:
            if client != self:
                client.send(message)

    def on_close(self):
        self.clients.remove(self)



