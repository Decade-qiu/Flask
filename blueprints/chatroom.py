import json
import datetime
from sockjs.tornado import SockJSConnection
from model.CRUD import CRUD


class ChatRoomHandler(SockJSConnection):
    waiters = set()

    def on_open(self, request):
        self.waiters.add(self)

    def on_message(self, message):
        try:
            data = json.loads(message)
            streamid = data.get('streamid', '')
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_msg(content, streamid)
            self.broadcast(self.waiters, content)
        except Exception as e:
            print(e)

    # 3.关闭连接
    def on_close(self):
        # 连接从连接池删除
        self.waiters.remove(self)



