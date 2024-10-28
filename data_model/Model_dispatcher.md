# process_feedback 函数的执行过程


self.bet_id_to_results 的变化是关键


self.bet_id_to_results：字典，键为 bet_id，值为另一个字典，记录了该 bet_id 下各个处理器的反馈结果。
在整个过程中，self.bet_id_to_results 的变化：
初始状态：

    bet_id_to_results = {}

    Handler A 反馈后：
    {
        1001: {1: True}
    }
    Handler B 反馈后：
    {
        1001: {1: True, 2: False}
    }
    Handler C 反馈后（收集齐所有结果）：
    {
        1001: {1: True, 2: False, 3: True}
    }

    清理后：
    {}
    完整情况下 bet_id_to_results:
    {
        bet_id1: {handler_id1: True, handler_id2: True, ...},
        bet_id2: {handler_id1: True, handler_id3: Flase, ...},
        ...
    }


 self.bet_id_to_handlers：字典，键为 bet_id，值为处理该 bet_id 的处理器信息列表，用于在发送指令时找到相关的处理器。
    {
        bet_id1: [handler_info1, handler_info2, ...],
        bet_id2: [handler_info1, handler_info3, ...],
        ...
    }
