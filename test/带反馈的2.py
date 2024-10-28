class Dispatcher:
    def __init__(self, handler_info_list, message_queue, feedback_queue):
        self.handler_info_list = handler_info_list
        self.message_queue = message_queue
        self.feedback_queue = feedback_queue
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
                # 轮询检查消息队列和反馈队列
                if not self.feedback_queue.empty():
                    feedback = self.feedback_queue.get()
                    self.process_feedback(feedback)
                if not self.message_queue.empty():
                    message_data = self.message_queue.get()
                    self.process_message(message_data)
            except Exception as e:
                print(f"[调度器] 运行时发生异常：{e}")

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
                    'instruction': 'instruction'  # 用于区分消息类型
                }
                handler_info['queue'].put(instruction)
            # 清理记录
            self.bet_id_to_results.pop(bet_id, None)
            self.bet_id_to_handlers.pop(bet_id, None)
