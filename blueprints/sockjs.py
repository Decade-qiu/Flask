import json
import datetime
import numpy as np
from sockjs.tornado import SockJSConnection
import tornado
from model.CRUD import CRUD


class ChatRoomHandler(SockJSConnection):
    # waiters = set()
    dic = dict()
    def on_open(self, request):
        room = int(request.arguments.get('streamid', '')[0], 10)
        if room not in self.dic:
            self.dic[room] = set()
        self.dic[room].add(self)
       
    def on_message(self, message):
        try:
            data = json.loads(message)
            streamid = data.get('streamid', '')
            print(streamid)
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_msg(content, streamid)
            if streamid != '':
                self.broadcast(self.dic[int(streamid)], content)
        except Exception as e:
            print(e, "11111")
    def on_close(self):
        # self.dic[room].remove(self)
        pass

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

class AudioHandler(SockJSConnection):   
    dic = dict()
    def on_open(self, info):
        room = int(info.arguments.get('streamid', '')[0], 10)
        if room not in self.dic:
            self.dic[room] = set()
        self.dic[room].add(self)
        print(room, self.dic[room])

    def on_message(self, message):
        # print(type(message), message)
        data = json.loads(message)
        uid = data['sid']
        url = data['url']
        for conn in self.dic[int(uid)]:
            conn.send(url)

    def on_close(self):
        pass

class CommentHandler(SockJSConnection):
    # waiters = set()
    dic = dict()
    def on_open(self, request):
        room = int(request.arguments.get('courseid', '')[0], 10)
        if room not in self.dic:
            self.dic[room] = set()
        self.dic[room].add(self)
       
    def on_message(self, message):
        try:
            data = json.loads(message)
            streamid = data.get('streamid', '')
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_con(content, streamid)
            if streamid != '':
                self.broadcast(self.dic[int(streamid)], content)
        except Exception as e:
            print(e, "11111")
    def on_close(self):
        # self.dic[room].remove(self)
        pass

class CCHandler(SockJSConnection):
    # waiters = set()
    dic = dict()
    def on_open(self, request):
        room = int(request.arguments.get('courseid', '')[0], 10)
        if room not in self.dic:
            self.dic[room] = set()
        self.dic[room].add(self)
       
    def on_message(self, message):
        try:
            data = json.loads(message)
            streamid = data.get('courseid', '')
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_cc(content, streamid)
            if streamid != '':
                self.broadcast(self.dic[int(streamid)], content)
        except Exception as e:
            print(e, "11111")
    def on_close(self):
        # self.dic[room].remove(self)
        pass


class checkHandler(SockJSConnection):   

    connections = set()

    def on_open(self, info):
        self.connections.add(self)
        print("open!!")

    def on_message(self, message):
        for conn in self.connections:
            if conn != self:
                conn.send(message)

    def on_close(self):
        self.connections.remove(self)
        print("close!!")