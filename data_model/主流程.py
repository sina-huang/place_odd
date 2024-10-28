# todo 基础数据准备
# ws接收到的数据
ws_message={
  "message": {
    "bet_id": 1001,
    "home_max_odds": {
      "odds": 2.9,
      "Platform": "Rollbit",
      "game_name": "Game A",
      "standard_name": "Standard Game A"
    },
    "draw_max_odds": {
      "odds": 3.15,
      "Platform": "Stake",
      "game_name": "Game A",
      "standard_name": "Standard Game A"
    },
    "away_max_odds": {
      "odds": 3.2,
      "Platform": "Rollbit",
      "game_name": "Game A",
      "standard_name": "Standard Game A"
    },
    "total_odds": 0.974787903667214
  }
}
# ads浏览器启动和网址等信息
hander_info_list = [
        {
            'process': 'Stake进程对象1',
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
        }]


# todo 构建出来的数据结构
# 这个是要发送给调度器的数据
handler_info_list = [
    {
        'platform_name': 'Rollbit',
        'handler_id': 0,
        'queue': handler_queue_0,
    },
    {
        'platform_name': 'Stake',
        'handler_id': 1,
        'queue': handler_queue_1,
    },...
    # 可能还有其他处理器实例
]

