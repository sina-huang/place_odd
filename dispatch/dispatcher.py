# Model_dispatcher.py

from multiprocessing import Queue
import json

'''
代码逻辑已经较为复杂，使用的数据结构也很多，可以查询data_model文件夹中的数据结构进行对比
'''
class Dispatcher:
    def __init__(self, handler_info_list, message_queue):
        self.handler_info_list = handler_info_list
        self.message_queue = message_queue
        self.platform_handler_counters = {}
        # 构建平台与处理器的映射
        self.platform_to_handlers = {}
        for handler_info in self.handler_info_list:
            platform_name = handler_info['platform_name']
            self.platform_to_handlers.setdefault(platform_name, []).append(handler_info)

    def run(self):
        while True:
            try:
                # 获取来自 Receiver 的消息
                message_data = self.message_queue.get()
                self.process_message(message_data)
            except Exception as e:
                print(f"[调度器] 运行时发生异常：{e}")

    def process_message(self, message_data):
        # 解析消息
        try:
            message = json.loads(message_data)
            print(f'[调度器 收到message:] {message}')
        except json.JSONDecodeError as e:
            print(f"[调度器] JSON解析消息时发生异常：{e}")
        # 收集每个平台的所有条目
        platform_entries = {}
        for key in ['home_max_odds', 'draw_max_odds', 'away_max_odds']:
            if key in message:
                entry = message[key]
                platform_name = entry['Platform']
                platform_entries.setdefault(platform_name, []).append(entry)

        # 分配消息给处理器实例
        for platform_name, entries in platform_entries.items():
            handlers = self.platform_to_handlers.get(platform_name, [])
            if handlers:
                num_handlers = len(handlers)
                # 获取该平台的当前计数器
                counter = self.platform_handler_counters.get(platform_name, 0)
                # 在同一条消息内轮询分配
                for i, entry in enumerate(entries):
                    handler_index = (counter + i) % num_handlers
                    handler_info = handlers[handler_index]
                    handler_queue = handler_info['queue']
                    handler_queue.put(entry)
                # 更新计数器
                self.platform_handler_counters[platform_name] = counter + len(entries)
            else:
                print(f"未找到平台 {platform_name} 的处理器")


