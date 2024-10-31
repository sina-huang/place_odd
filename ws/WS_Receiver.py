from utils.Log import get_logger
from ws.WebSocketThread import WebSocketThread
from settings import WS
import json


class Receiver(WebSocketThread):
    def __init__(self,message_queue, url=WS['url_betting'],log_file_name=None):
        self.num = 0
        # 动态生成日志文件名，例如 "Receiver.log"
        self.log_file_name = log_file_name or f'./Log/{self.__class__.__name__}.log'

        self.logger = get_logger(name=__name__, log_file=self.log_file_name)

        self.message_queue = message_queue

        # 调用父类初始化，并传递 logger
        super().__init__(url, logger=self.logger)

    def on_message(self, ws, message):
        self.logger.warning(f"[收到消息]：{message}")
        try:
            data_str=self.parse_ws_message(message)
            self.message_queue.put(data_str)
        except Exception as e:
            self.logger.error(f"[发布消息错误]：{e}")

    def parse_ws_message(self, data):
        try:
            message_dict = json.loads(data)
            data_str = message_dict.get('message')

            # 处理 message 的不同类型
            if isinstance(data_str, str):
                # 如果 data_str 是字符串，将其转换为字典
                data_dict = json.loads(data_str)
            elif isinstance(data_str, dict):
                # 如果 data_str 已经是字典，则直接使用
                data_dict = data_str
            else:
                # 如果 message 既不是字符串也不是字典，打印日志并返回 None
                print('WebSocket message 格式不正确，未识别的数据类型:', type(data_str))
                return None
            data_dict['bet_id'] = self.num
            self.num += 1
            # 返回 JSON 格式字符串

            return json.dumps(data_dict)
        except json.JSONDecodeError as e:
            print('WebSocket 解析错误:', e)
            return None
