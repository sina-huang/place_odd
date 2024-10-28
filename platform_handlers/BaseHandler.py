# platform_handlers/base_handler.py
import time
from abc import ABC, abstractmethod
from DrissionPage import ChromiumPage, ChromiumOptions
import multiprocessing
import queue


class BaseHandler(ABC):
    def __init__(self, info, message_queue, config=None):
        if config is None:
            config = {'refresh_rate': 0.5, 'message_check_interval': 0.1, 'page_check_interval': 5}
        self.refresh_rate = config['refresh_rate']
        self.message_check_interval = config['message_check_interval']
        self.page_check_interval = config['page_check_interval']

        # 获取配置信息
        self.debug_port = info['debug_port']
        self.start_url = info['start_url']
        self.platform_name = info['platform_name']
        self.handler_id = info['handler_id']   # 可以理解为自定义进程ID

        # 消息队列
        self.message_queue = message_queue

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
                # print(f"{self.__class__.__name__} 收到消息: {message}")
                if message is None:
                    # 可以在这里处理退出逻辑
                    break
                else:
                    self.place_bet(message)
            except queue.Empty:
                # 队列为空，超时，可以进行其他操作
                pass
            except Exception as e:
                print(f"[{self.platform_name}] 运行时发生异常：{e}")

            current_time = time.time()
            if current_time - last_page_check_time >= self.page_check_interval:
                last_page_check_time = current_time
                # if not self.page or self.page.is_closed:
                #     print(f"[{self.platform_name}] 页面失效，正在重新初始化浏览器...")
                #     self.initialize_browser()
            # 控制循环的休眠时间，防止 CPU 占用过高
            time.sleep(self.message_check_interval)




    def initialize_browser(self):
        try:
            # todo 给配置对象设置debug_port
            if not hasattr(self.chrome_option, 'debug_port') or not self.chrome_option.debug_port:
                self.chrome_option.set_local_port(self.debug_port)

            # todo 新建浏览器对象
            if not self.chrome:
                self.chrome = ChromiumPage(addr_or_opts=self.chrome_option)

            # todo 新建page对象
            self.page = self.chrome.new_tab(self.start_url)
            self.prepare_page(self.page)

        except Exception as e:
            self.chrome = None
            print(f"初始化浏览器时出错：{e}")


    @abstractmethod
    def place_bet(self, bet_info):
        raise NotImplementedError


    @abstractmethod
    def prepare_page(self, page):
        """在页面加载后进行必要的准备工作，如登录、切换语言等"""
        pass



