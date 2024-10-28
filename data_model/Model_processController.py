platform_configs = Sample_of_data = {
    'knbvol0': {
        'Rollbit': {
            'class': 'platform_handlers.rollbit_handler.RollbitHandler',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        },
        'Stake': {
            'class': 'platform_handlers.stake_handler.StakeHandler',
            'platform_name': 'Stake',
            'start_url': 'https://stake.com/zh/sports/live/soccer'
        }
    },
    'ko5eksd': {
        'Rollbit': {
            'class': 'platform_handlers.rollbit_handler.RollbitHandler',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        },
        'Stake': {
            'class': 'platform_handlers.stake_handler.StakeHandler',
            'platform_name': 'Stake',
            'start_url': 'https://stake.com/zh/sports/live/soccer'
        }
    }
}

# todo  执行for debug_port, platforms in self.platform_configs.items():
debug_port = 'ko5eksd'
platforms = {
        'Rollbit': {
            'class': 'platform_handlers.rollbit_handler.RollbitHandler',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        },
        'Stake': {
            'class': 'platform_handlers.stake_handler.StakeHandler',
            'platform_name': 'Stake',
            'start_url': 'https://stake.com/zh/sports/live/soccer'
        }
    }

# todo 执行 for platform_name, handler_info in platforms.items():
platform_name = 'Rollbit'
handler_info = {
            'class': 'platform_handlers.rollbit_handler.RollbitHandler',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        }

# todo 所以这里开始组装新的字典
info = {
        'debug_port': 22222,
        'platform_name': handler_info['platform_name'],
        'start_url': handler_info['start_url'],
        'handler_id': 0,
}

# todo  将info 和新建的队列作为参数传入 handler_class，这个handler_class就是handler_info['class']

# todo 执行完之后会生成一个handler_info_list，这是一个进程列表，进程都装在里面了
hander_info_list = [
{
    'process': 'Process对象1',
    'platform_name': 'Stake',
    'queue': 'Queue对象1',  # 处理器实例1的消息队列
    'handler_id': 0,
},
{
    'process': 'Process对象2',
    'platform_name': 'Rollbit',
    'queue': 'Queue对象2',  # 处理器实例2的消息队列
    'handler_id': 1,
},
{
    'process': 'Process对象3',
    'platform_name': 'Rollbit',
    'queue': 'Queue对象3',  # 处理器实例3的消息队列
    'handler_id': 2,
},
# ... 可能有更多的处理器实例
]