from channels.generic.websocket import WebsocketConsumer
import json

class ListDataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
    	# 字典化接收数据
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 数据处理
        self.send(text_data=json.dumps({
        'feedback': "Accept",
        # 返回数据
    }))
