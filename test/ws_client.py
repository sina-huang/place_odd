# websocket_client.py

import asyncio
import websocket
import json
from platform_handlers import get_platform_handler



import time
import json
import websocket
import queue
import logging

logger = logging.getLogger(__name__)


class WebSocketHandler:

    def __init__(self, ws_url, queue, manager, platform_name,check_online_time=10):
        """
        :param ws_url: ws地址，字符串
        :param queue: 挂载主进程中的队列
        :param manager: 挂载主进程对象本身
        """
        self.ws_url = ws_url
        self.ws = None
        self.queue = queue
        self.Platform = platform_name
        self.manager = manager  # 引用管理器以共享变量
        self.last_received_time = time.time()
        self.last_log_time = 0  # 初始化上次日志打印时间
        self.last_log_time_= 0
        self.check_online_time = check_online_time

    def connect_websocket(self):
        # 在这里定义回调函数
        def on_message(ws, message):
            self.last_received_time = time.time()
            # logger.info(f"收到服务器返回数据: {message}")
            try:
                data = json.loads(message)
                if 'message' in data:
                    real_data = data['message']
                    if isinstance(real_data, str):
                        real_data = json.loads(real_data)
                    platform = real_data.get('Platform', '')
                    if platform == self.Platform:
                        with self.manager.lock:
                            self.manager.last_received_time = time.time()
                            logger.info(f"[{self.Platform}平台] [收到信息] 已更新时间")

                            # 检查是否超过了 10 秒
                            current_time = time.time()
                            if current_time - self.last_log_time >= self.check_online_time:
                                logger.warning(f"[{self.check_online_time} 秒掉线侦测] [{self.Platform} 平台]--[通信正常]")
                                self.last_log_time = current_time
                                self.last_log_time_ = current_time

                    current_time = time.time()
                    if current_time - self.last_log_time_ >= self.check_online_time * 2:
                        logger.warning(f"[{self.check_online_time*2} 秒掉线检查] ----> WS可能掉线")
                        logger.warning("若是启动阶段，则可忽视此消息")
                        logger.warning("若非启动阶段，需要重新启动程序！！！！")
                        self.last_log_time_ = current_time

            except Exception as e:
                logger.error(f"[{self.Platform}平台] 解析服务器返回数据时出现异常: {e}")

        def on_error(ws, error):
            logger.error(f"[{self.Platform}平台] WebSocket 出现错误: {error}")
            self.ws = None  # 确保重新连接

        def on_close(ws, close_status_code, close_msg):
            logger.warning(f"[{self.Platform}平台] WebSocket 连接关闭，尝试重新连接...")
            self.ws = None  # 确保重新连接

        def on_open(ws):
            logger.warning(f"[{self.Platform}平台] WebSocket 已连接成功！")

        while True:
            if self.ws is None:
                try:
                    self.ws = websocket.WebSocketApp(
                        self.ws_url,
                        on_open=on_open,
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close
                    )
                    logger.info(f"[{self.Platform}平台] WebSocket 正在连接...")
                    self.ws.run_forever()
                except Exception as e:
                    logger.error(f"[{self.Platform}平台] WebSocket 连接失败: {e}")
                finally:
                    self.ws = None
                    time.sleep(5)
            else:
                time.sleep(1)

    def send_data(self, data):
        while self.ws is None:
            logger.warning(f"[{self.Platform}平台] WebSocket 未连接，等待连接...")
            time.sleep(1)
        try:
            json_data = json.dumps(data, ensure_ascii=False)

            self.ws.send(json_data)
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            logger.info(f" [{self.Platform}平台] [发送数据]{json_str} ")
        except Exception as e:
            logger.error(f"[{self.Platform}平台] 发送数据失败: {e}")
            self.ws = None  # 确保重新连接

    def run(self):
        # 该方法不再创建新线程，只处理队列中的数据
        while True:
            try:
                data = self.queue.get(timeout=10)
                if data is None:
                    continue
                self.send_data(data)
                self.queue.task_done()
            except queue.Empty:
                logger.warning(f"[{self.Platform}平台] 管道为空，爬虫慢，等待中...")
            except Exception as e:
                logger.error(f"[{self.Platform}平台] WebSocketHandler 运行过程中出现异常: {e}")

