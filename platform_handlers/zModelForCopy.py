import threading
import time
import sys

# 导入您的 RollbitHandler 类
from platform_handlers.BaseHandler import BaseHandler
from utils.Log import get_logger

# 测试导入包
from DrissionPage import ChromiumPage, ChromiumOptions
from settings import ADS
import requests

# 如果在 Windows 平台上
if sys.platform.startswith('win'):
    import msvcrt
else:
    # 在 Unix/Linux 平台上
    import tty
    import termios

class RollbitHandler(BaseHandler):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        self.platform_name = 'Rollbit'
        self.handler_id = info.get('handler_id', '未分配进程ID号')
        self.log_name = f'./Log/{self.platform_name}_{self.handler_id}.log'

        self.logger = get_logger(name=f'{self.platform_name}_{self.handler_id}', log_file=self.log_name,
                                 file_mode='a')

        super().__init__(info, message_queue, feedback_queue, config, platform_name=self.platform_name)

    def click_bet_button_by_team_name(self):
        # 示例函数，打印一条信息
        print(f"[{self.platform_name}--{self.handler_id}] 执行了 click_bet_button_by_team_name()")
        # 这里可以添加您的实际代码逻辑
        return True

    def compare_and_verify_bet_odds(self):
        print(f"[{self.platform_name}--{self.handler_id}] 执行了 compare_and_verify_bet_odds()")
        return True

    def place_bet(self):
        print(f"[{self.platform_name}--{self.handler_id}] 下单成功")
        pass

    def cancel_bet(self, bet_id):
        print(f"[{self.platform_name}--{self.handler_id}] 取消订单")
        pass

    def prepare_page(self, page):
        pass

# 定义一个函数，用于监听用户输入
def listen_for_input(rollbit_handler):
    # 定义按键与函数的映射
    key_function_map = {
        '1': rollbit_handler.click_bet_button_by_team_name,
        '2': rollbit_handler.compare_and_verify_bet_odds,
        '3': rollbit_handler.place_bet,
        # 可以添加更多的按键映射
    }

    print("请按下对应的数字键以执行函数：")
    print("1 - click_bet_button_by_team_name()")
    print("2 - compare_and_verify_bet_odds()")
    print("3 - place_bet()")
    print("按 'q' 键退出监听。")

    while True:
        # 获取用户输入的按键
        if sys.platform.startswith('win'):
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
        else:
            # Unix/Linux 平台上的非阻塞输入实现
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if key == 'q':
            print("退出监听。")
            break
        elif key in key_function_map:
            func = key_function_map[key]
            print(f"按下了键 '{key}'，将执行函数 {func.__name__}()")
            try:
                func()
            except Exception as e:
                print(f"执行函数时发生错误：{e}")
        else:
            print(f"按下了未知的键 '{key}'，请按有效的数字键。")
        time.sleep(0.1)

if __name__ == '__main__':
    ads_id = 'knbvol0'
    ads_open_url = ADS['ads_open_url'] + ads_id
    resp = requests.get(ads_open_url).json()
    time.sleep(2)
    if resp["code"] != 0:
        print(f'[ads 启动失败] ads_id: {ads_id},处理办法: 需要确保两个 ads 浏览器请求之间的时间间隔，如果间隔太短，ads 浏览器会启动失败')
    debug_port = int(resp["data"]["debug_port"])

    rollbit_handler = RollbitHandler(
        info={
            'handler_id': '123',
            'debug_port': debug_port,
            'start_url': 'https://rollbit.com/sports?bt-path=%2Flive'
        },
        message_queue=None,
        feedback_queue=None,
        config=None
    )

    # 创建并启动监听用户输入的线程
    input_thread = threading.Thread(target=listen_for_input, args=(rollbit_handler,))
    input_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    input_thread.start()

    # 在主线程中运行 rollbit_handler
    try:
        rollbit_handler.run()
    except KeyboardInterrupt:
        print("主程序收到退出指令，正在关闭...")
