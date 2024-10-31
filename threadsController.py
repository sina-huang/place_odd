# processing_controller.py

from multiprocessing import Process, Queue,Manager
import time
from config import get_platform_configs
from dispatch.dispatcher import Dispatcher
from ws.WS_Receiver import Receiver


def dispatcher_process_run(handler_info_list, receiver_queue, feedback_queue):
    dispatcher = Dispatcher(handler_info_list, receiver_queue, feedback_queue)
    dispatcher.run()


def start_handler_process(handler_class, info, message_queue, feedback_queue):
    # 在子进程中创建处理器实例
    handler = handler_class(info=info, message_queue=message_queue, feedback_queue=feedback_queue)
    # 调用处理器的运行方法
    handler.run()

class ProcessingController:
    def __init__(self):
        self.manager = Manager()
        self.receiver = None
        self.handler_info_list = []
        # todo 启动时用于必须要使用的数据结构，包括：ads_id，类的调用，平台名字，启动url
        self.platform_configs = get_platform_configs()

        # todo 初始化两个队列
        self.receiver_queue = self.manager.Queue()  # 用于接收 Receiver 的消息
        self.feedback_queue = self.manager.Queue()  # 新增反馈队列

        # todo 启动各类进程
        self.start_browser_processes()
        self.start_dispatcher_processes()
        self.start_receiver_threading()

    def start_browser_processes(self):
        handler_id_counter = 0
        for debug_port, platforms in self.platform_configs.items():
            for platform_name, handler_info in platforms.items():
                # 合并配置信息
                info = {
                    'debug_port': debug_port,
                    'platform_name': handler_info['platform_name'],
                    'start_url': handler_info['start_url'],
                    'handler_id': handler_id_counter,
                    # 可以添加更多配置项
                }
                handler_id_counter += 1
                handler_class = handler_info['class']  # 拿到类对象
                # 创建消息队列
                handler_queue = self.manager.Queue()
                # 不在主进程中创建处理器实例
                # handler = handler_class(info=info, message_queue=handler_queue, feedback_queue=self.feedback_queue)
                # 启动处理器进程
                p = Process(target=start_handler_process,
                            args=(handler_class, info, handler_queue, self.feedback_queue))
                p.daemon = True
                p.start()
                # 保存处理器信息
                self.handler_info_list.append({
                    'platform_name': platform_name,
                    'handler_id': info['handler_id'],
                    'queue': handler_queue,
                })

    def start_dispatcher_processes(self):
        # todo 调度类，接收
        dispatcher_process = Process(target=dispatcher_process_run,
                                     args=(self.handler_info_list, self.receiver_queue, self.feedback_queue))
        dispatcher_process.daemon = True
        dispatcher_process.start()

    def start_receiver_threading(self):
        # 启动 Receiver 线程,这里收到的消息会直接发送到receiver_queue 这个队列中。他是逻辑上的第一步
        # todo 这里的写法不同于上面两个，是因为我的Receiver类是继承了threading.Thread，所以会自己开启线程。这里不需要再额外启动线程
        self.receiver = Receiver(self.receiver_queue)
        self.receiver.start()

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("主程序收到退出指令，正在关闭...")

if __name__ == "__main__":
    controller = ProcessingController()
    controller.run()
