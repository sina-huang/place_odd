import time
import queue
from abc import ABC, abstractmethod
from DrissionPage import ChromiumPage, ChromiumOptions

class BaseHandler(ABC):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        if config is None:
            config = {
                'refresh_rate': 0.5,
                'message_check_interval': 0.1,
                'page_check_interval': 5
            }
        self.refresh_rate = config['refresh_rate']
        self.message_check_interval = config['message_check_interval']
        self.page_check_interval = config['page_check_interval']

        # 获取配置信息
        self.debug_port = info['debug_port']
        self.start_url = info['start_url']
        self.platform_name = info['platform_name']
        self.handler_id = info['handler_id']  # 唯一的处理器 ID

        # 消息队列
        self.message_queue = message_queue  # 接收投注信息和指令
        self.feedback_queue = feedback_queue  # 发送反馈给调度器

        # 管理投注
        self.pending_bets = {}  # 存储待处理的投注信息

        # 浏览器配置项
        self.page = None
        self.chrome_option = None
        self.chrome = None

    def run(self):
        self.chrome_option = ChromiumOptions()
        self.chrome_option.set_local_port(self.debug_port)
        self.initialize_browser()  # 启动浏览器

        last_page_check_time = time.time()

        while True:
            try:
                # 从消息队列获取消息
                message = self.message_queue.get(timeout=self.message_check_interval)

                if message is None:
                    break
                else:
                    message_type = message.get('type')
                    if message_type == 'instruction':
                        # 处理来自调度器的指令
                        print(f"[{self.platform_name}-{self.handler_id}] 收到下单指令：{message}")
                        self.receive_instruction(message)
                    else:
                        # 处理ws信息
                        print(f"[{self.platform_name}-{self.handler_id}] 收到ws信息：{message}")
                        self.handle_bet_message(message)
            except queue.Empty:
                pass  # 队列为空，继续循环
            except Exception as e:
                print(f"[{self.platform_name}] 运行时发生异常：{e}")

            # 处理待处理的投注
            self.process_pending_bets()

            # 定期检查页面状态
            current_time = time.time()
            if current_time - last_page_check_time >= self.page_check_interval:
                last_page_check_time = current_time
                if not self.page:
                    print(f"[{self.platform_name}] 页面失效，正在重新初始化浏览器...")
                    self.initialize_browser()
            # 控制循环的休眠时间，防止 CPU 占用过高
            time.sleep(0.01)

    def initialize_browser(self):
        try:
            # 设置调试端口
            if not hasattr(self.chrome_option, 'debug_port') or not self.chrome_option.debug_port:
                self.chrome_option.set_local_port(self.debug_port)

            # 创建浏览器对象
            if not self.chrome:
                self.chrome = ChromiumPage(addr_or_opts=self.chrome_option)

            # 打开新页面
            self.page = self.chrome.new_tab(self.start_url)
            self.prepare_page(self.page)

        except Exception as e:
            self.chrome = None
            print(f"[{self.platform_name}] 初始化浏览器时出错：{e}")

    def handle_bet_message(self, message):
        bet_id = message.get('bet_id')
        # todo 自动化脚本需要自己去检查赔率，并返回 True 或 False
        can_place_bet = self.check_odds(message)
        # 发送检查结果给调度器
        feedback = {
            'handler_id': self.handler_id,
            'bet_id': bet_id,
            'can_place_bet': can_place_bet,
            'platform_name': self.platform_name
        }
        self.feedback_queue.put(feedback)
        # 将投注信息存储到待处理列表中
        self.pending_bets[bet_id] = {
            'message': message,
            'status': 'waiting'  # 等待调度器的指令
        }

    def receive_instruction(self, instruction):
        bet_id = instruction.get('bet_id')
        action = instruction.get('action')
        # 更新待处理投注的状态
        if bet_id in self.pending_bets:
            self.pending_bets[bet_id]['action'] = action
            self.pending_bets[bet_id]['status'] = 'ready'  # 可以执行了

    def process_pending_bets(self):
        to_remove = []
        for bet_id, bet_info in self.pending_bets.items():
            if bet_info['status'] == 'ready':
                action = bet_info.get('action')
                message = bet_info.get('message')
                if action == 'proceed':
                    self.place_bet(message)
                elif action == 'cancel':
                    self.cancel_bet(bet_id)
                # 处理完毕，标记为待移除
                to_remove.append(bet_id)
        # 移除已处理的投注
        for bet_id in to_remove:
            self.pending_bets.pop(bet_id, None)

    @abstractmethod
    def check_odds(self, bet_info):
        """执行赔率检查，返回 True 或 False"""
        pass

    @abstractmethod
    def place_bet(self, bet_info):
        """执行下单操作"""
        pass

    @abstractmethod
    def cancel_bet(self, bet_id):
        """执行取消下单的操作"""
        bet_info = self.pending_bets.get(bet_id)
        pass

    @abstractmethod
    def prepare_page(self, page):
        """初始化页面，例如登录、导航到特定页面"""
        pass
