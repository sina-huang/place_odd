hander_info_list = [
{
    'process': 'Process进程对象1',
    'platform_name': 'Stake',
    'queue': 'Queue对象1',  # 处理器实例1的消息队列
    'handler_id': 0,
},
{
    'process': 'Process进程对象2',
    'platform_name': 'Rollbit',
    'queue': 'Queue对象2',  # 处理器实例2的消息队列
    'handler_id': 1,
},
{
    'process': 'Process进程对象3',
    'platform_name': 'Rollbit',
    'queue': 'Queue对象3',  # 处理器实例3的消息队列
    'handler_id': 2,
},
# ... 可能有更多的处理器实例
]
 # todo 根据hander_info_list组装成了一个新的字典，其中包含每个平台的消息队列和处理器实例
platform_to_handlers = {
    'Stake': [
        {
            'process': 'Process对象1',
            'platform_name': 'Stake',
            'queue': 'Queue对象1',
            'handler_id': 0,
        },
        # 可能有更多 Stake 平台的处理器实例
    ],
    'Rollbit': [
        {
            'process': 'Process对象2',
            'platform_name': 'Rollbit',
            'queue': 'Queue对象2',
            'handler_id': 1,
        },
        {
            'process': 'Process对象3',
            'platform_name': 'Rollbit',
            'queue': 'Queue对象3',
            'handler_id': 2,
        },
        # 可能有更多 Rollbit 平台的处理器实例
    ],
    # 其他平台
}

platform_handler_counters = {
    'Stake': 5,  # Stake 平台已经分配了 5 条消息
    'Rollbit': 10,  # Rollbit 平台已经分配了 10 条消息
    # 其他平台
}

message = {
    "home_max_odds": {
        "odds": 2.9,
        "Platform": "Rollbit",
        "game_name": "Kaya FC–Iloilo -- Eastern SC",
        "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
    "draw_max_odds": {
        "odds": 3.15,
        "Platform": "Stake",
        "game_name": "Kaya FC–Iloilo -- Eastern Sports Club",
        "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
    "away_max_odds": {
        "odds": 3.2,
        "Platform": "Rollbit",
        "game_name": "Kaya FC–Iloilo -- Eastern SC",
        "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
    "total_odds": 0.974787903667214
}
# todo process_message函数

# todo 根据message的值，提取出新的结构entries，只包含了message下单的信息
entries = [
    {
        "odds": 2.9,
        "Platform": "Rollbit",
        "game_name": "Kaya FC–Iloilo -- Eastern SC",
        "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
    {
            "odds": 3.15,
            "Platform": "Stake",
            "game_name": "Kaya FC–Iloilo -- Eastern Sports Club",
            "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
    {
            "odds": 3.2,
            "Platform": "Rollbit",
            "game_name": "Kaya FC–Iloilo -- Eastern SC",
            "standard_name": "Kaya FC–Iloilo -- Eastern SC"
    },
]
# todo 遍历entries，
entry = {
            "odds": 3.2,
            "Platform": "Rollbit",
            "game_name": "Kaya FC–Iloilo -- Eastern SC",
            "standard_name": "Kaya FC–Iloilo -- Eastern SC"
        } or \
        {
            "odds": 3.15,
            "Platform": "Stake",
            "game_name": "Kaya FC–Iloilo -- Eastern Sports Club",
            "standard_name": "Kaya FC–Iloilo -- Eastern SC"
        }

# todo 拿到entry，根据平台名称，去platform_to_handlers中找对应的处理器实例，得到handlers
handlers = [
        {
            'process': 'Process对象2',
            'platform_name': 'Rollbit',
            'queue': 'Queue对象2',
            'handler_id': 1,
        },
        {
            'process': 'Process对象3',
            'platform_name': 'Rollbit',
            'queue': 'Queue对象3',
            'handler_id': 2,
        },
        # 可能有更多 Rollbit 平台的处理器实例
    ]



