# todo 启动浏览器需要的数据结构，包括：ads_id，启动url，需要调用的类，平台名称
handler_info_list ={
    'knbvol0': {
        'Rollbit': {
            'class': 'RollbitHandler类',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        },
        'Stake': {
            'class': 'StakeHandler类',
            'platform_name': 'Stake',
            'start_url': 'https://stake.com/zh/sports/live/soccer'
        }
    },
    'ko5eksd': {
        'Rollbit': {
            'class': 'RollbitHandler类',
            'platform_name': 'Rollbit',
            'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'
        },
        'Stake': {
            'class': 'StakeHandler类',
            'platform_name': 'Stake',
            'start_url': 'https://stake.com/zh/sports/live/soccer'
        }
    }
}

# todo 在initialize_processes() 中，构造了一个新的数据结构

    # todo info字典
info = {
        'debug_port': 22222,
        'platform_name': 'Stake',
        'start_url': '启动url',
        'handler_id': 0,
}
    # todo 构建实例 handler，传入了info，属于handler自己的queue，以及一个公用的feedback_queue
#  handler = handler_class(info=info, message_queue=handler_queue, feedback_queue=self.feedback_queue)

