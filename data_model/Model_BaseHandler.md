不断地从message_queue中取出消息
注意这里的message_queue 是单对单的，也就是说调度器和处理器之间永远都是一对一的
调度器经过分析之后，通过不同的message_queue发送信号，每个对象都有一个自己专属的message_queue

-------------------------调度器发送给我的数据--------------------------
message = {
    'bet_id': 1001,
    'odds': 2.9,
    'Platform': 'Rollbit',
    'game_name': 'Game A',
    'standard_name': 'Standard Game A'
}

instruction = {
    'bet_id': 1001,
    'action': 'proceed',  # 或 'cancel'
    'instruction': 'instruction'
}
-------------------------我发送给调度器的数据--------------------------
feedback = {
            'handler_id': self.handler_id,
            'bet_id': 1001,
            'can_place_bet': True or False,
            'platform_name': 'Rollbit'
        }


---------------------------自己的数据结构-------------------------
pending_bets = {
    bet_id1: {
        'message': bet_message1,
        'status': 'waiting' or 'ready',
        'action': 'proceed' or 'cancel' (当 status 为 'ready' 时存在)
    },
    bet_id2: {
        'message': bet_message2,
        'status': 'waiting',
    },
    # 更多待处理的投注
}

---------------------------执行过程-------------------------

message = {
    'bet_id': 1001,
    'odds': 2.9,
    'Platform': 'Rollbit',
    'game_name': 'Game A',
    'standard_name': 'Standard Game A'
} 
进入，经过处理之后，会发送数据给调度器，如：
        {
            'handler_id': self.handler_id,
            'bet_id': 1001,
            'can_place_bet': True or False,
            'platform_name': 'Rollbit'
        }
内部的pending_bets 变成了
{
    1001: {
        'message': message,
        'status': 'waiting'
    }
}

步骤 3：处理器收到调度器的指令
instruction = {
    'bet_id': 1001,
    'action': 'proceed',  # 或 'cancel'
    'instruction': 'instruction'
}
执行 self.receive_instruction(instruction)
更新 pending_bets 中对应投注的状态和指令：
{
    1001: {
        'message': message,
        'status': 'ready',
        'action': 'proceed'
    }
}
bet_id = 1001：
status 为 'ready'，获取 action 和 message。
如果 action == 'proceed'，执行 self.place_bet(message)。
如果 action == 'cancel'，执行 self.cancel_bet(bet_id)。

结束！！！！ 逻辑上是没有问题了