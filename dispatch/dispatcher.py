# Model_dispatcher.py

from multiprocessing import Queue
import json
import queue
import time
from  pprint import pprint
'''
代码逻辑已经较为复杂，使用的数据结构也很多，可以查询data_model文件夹中的数据结构进行对比
'''
class Dispatcher:
    def __init__(self, handler_info_list, receiver_queue, feedback_queue):
        """
        :param handler_info_list: 所有的处理器信息，包括处理器名称、处理器编号、处理器自己的管道
        :param receiver_queue: 主进程接收数据管道
        :param feedback_queue: 主进程回馈数据管段
        """

        self.handler_info_list = handler_info_list
        self.receiver_queue = receiver_queue
        self.feedback_queue = feedback_queue

        # todo : 添加其他初始化内容
        self.platform_handler_counters = {}
        # 构建平台与处理器的映射
        self.platform_to_handlers = {}
        for handler_info in self.handler_info_list:
            platform_name = handler_info['platform_name']
            self.platform_to_handlers.setdefault(platform_name, []).append(handler_info)
        # 存储 bet_id 对应的处理器和检查结果
        self.bet_id_to_handlers = {}
        self.bet_id_to_results = {}

    def run(self):
        while True:
            try:
                # 尝试从 feedback_queue 获取反馈，不阻塞
                feedback = self.feedback_queue.get_nowait()
                self.process_feedback(feedback)
            except queue.Empty:
                pass  # 队列为空，继续其他操作
            except Exception as e:
                print(f"[调度器] 处理反馈时发生异常：{e}")

                # 同样地，处理来自 receiver_queue 的消息
            try:
                message_data = self.receiver_queue.get_nowait()
                pprint(f'[dispatch 收到ws消息]{message_data}')
                self.process_message(message_data)
            except queue.Empty:
                pass  # 队列为空，继续其他操作
            except Exception as e:
                print(f"[调度器] 处理消息时发生异常：{e}")

                # 为了防止 CPU 占用过高，可以适当休眠
            time.sleep(0.02)

    def process_message(self, message_data):
        try:
            message = json.loads(message_data)
        except json.JSONDecodeError as e:
            print(f"[调度器] JSON 解析错误：{e}")
            return
        bet_id = message.get('bet_id')
        platform_entries = {}
        for key in ['home_max_odds', 'draw_max_odds', 'away_max_odds']:
            if key in message:
                entry = message[key]
                platform_name = entry['Platform']
                platform_entries.setdefault(platform_name, []).append(entry)
        '''
        platform_entries = {
                'Rollbit': [
                    {
                        'odds': 2.9,
                        'Platform': 'Rollbit',
                        'game_name': 'Game A',
                        'standard_name': 'Standard Game A',
                        'bet_id': 1001  # 后面会添加
                    },
                    {
                        'odds': 3.2,
                        'Platform': 'Rollbit',
                        'game_name': 'Game A',
                        'standard_name': 'Standard Game A',
                        'bet_id': 1001  # 后面会添加
                    }
                ],
                'Stake': [
                    {
                        'odds': 3.15,
                        'Platform': 'Stake',
                        'game_name': 'Game A',
                        'standard_name': 'Standard Game A',
                        'bet_id': 1001  # 后面会添加
                    }
                ]
            }

        '''

        # 分配消息给处理器实例
        for platform_name, entries in platform_entries.items():
            handlers = self.platform_to_handlers.get(platform_name, [])
            if handlers:
                num_handlers = len(handlers)
                counter = self.platform_handler_counters.get(platform_name, 0)
                for i, entry in enumerate(entries):
                    handler_index = (counter + i) % num_handlers
                    handler_info = handlers[handler_index]
                    handler_queue = handler_info['queue']
                    # 添加 bet_id 到消息中
                    entry['bet_id'] = bet_id
                    handler_queue.put(entry)
                    # 记录 bet_id 到处理器的映射
                    self.bet_id_to_handlers.setdefault(bet_id, []).append(handler_info)
                self.platform_handler_counters[platform_name] = counter + len(entries)
            else:
                print(f"未找到平台 {platform_name} 的处理器")

    def process_feedback(self, feedback):
        '''
        :param feedback: {
                            'bet_id': 1001,
                            'handler_id': 1,
                            'can_place_bet': True,
                            'platform_name': 'Rollbit'
                        }
        主要这个函数构造了两个对象，
        self.bet_id_to_results：字典，键为 bet_id，值为另一个字典，记录了该 bet_id 下各个处理器的反馈结果。
        self.bet_id_to_handlers：字典，键为 bet_id，值为处理该 bet_id 的处理器信息列表，用于在发送指令时找到相关的处理器。
        '''

        bet_id = feedback.get('bet_id')
        handler_id = feedback.get('handler_id')
        can_place_bet = feedback.get('can_place_bet')
        # 记录检查结果
        results = self.bet_id_to_results.setdefault(bet_id, {})
        results[handler_id] = can_place_bet
        # 检查是否收集到了所有处理器的结果
        handlers = self.bet_id_to_handlers.get(bet_id, [])
        if len(results) == len(handlers):
            # 所有结果已收集，做出决策
            if all(results.values()):
                action = 'proceed'
            else:
                action = 'cancel'
            # 向所有处理器发送指令
            for handler_info in handlers:
                instruction = {
                    'bet_id': bet_id,
                    'action': action,
                    'type': 'instruction'  # 用于区分消息类型
                }
                # 这里handler_info_list 是将管道发送过来了的。
                handler_info['queue'].put(instruction)
            # 清理记录
            self.bet_id_to_results.pop(bet_id, None)
            self.bet_id_to_handlers.pop(bet_id, None)



