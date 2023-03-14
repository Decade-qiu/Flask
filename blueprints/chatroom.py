import json
import datetime
from sockjs.tornado import SockJSConnection
from model.CRUD import CRUD


class ChatRoomHandler(SockJSConnection):
    waiters = set()  # 去重

    # 1.建立连接
    def on_open(self, request):
        # 连接加入到连接池
        self.waiters.add(self)

    # 2.双向数据通信
    def on_message(self, message):
        try:
            # 处理消息，json格式，客户端设置
            data = json.loads(message)
            streamid = data.get('streamid', '')
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_msg(content, streamid)
            # 调用广播，把消息推送给所有的客户端
            self.broadcast(self.waiters, content)
        except Exception as e:
            print(e)

    # 3.关闭连接
    def on_close(self):
        # 连接从连接池删除
        self.waiters.remove(self)



