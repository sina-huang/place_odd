# platform_handlers/__init__.py
import requests

from settings import ADS,Platform
from platform_handlers.rollbit_handler import RollbitHandler
from platform_handlers.stake_handler import StakeHandler
# from config import get_platform_configs
from pprint import pprint




Sample_of_data = {2883: {
        'Rollbit': {'class': "class 'platform_handlers.rollbit_handler.RollbitHandler'",
                    'platform_name': 'Rollbit',
                    'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'},
        'Stake': {'class': "<class 'platform_handlers.stake_handler.StakeHandler'>",
                  'platform_name': 'Stake',
                  'start_url': 'https://stake.com/zh/sports/live/soccer'}},
 57824: {
        'Rollbit': {'class': "class 'platform_handlers.rollbit_handler.RollbitHandler'>",
                     'platform_name': 'Rollbit',
                     'start_url': 'https://rollbit.com/sports?bt-path=%2Fsoccer-1'},
         'Stake': {'class': "<class 'platform_handlers.stake_handler.StakeHandler'>",
                   'platform_name': 'Stake',
                   'start_url': 'https://stake.com/zh/sports/live/soccer'}
 }
}


# def platform_factory():
#     obj_list = []
#     platform_configs = get_platform_configs()  # 从 config.py 获取配置字典
#
#     for debug_port, platforms in platform_configs.items():
#         for platform_name, handler_info in platforms.items():
#             handler_class = handler_info['class']
#             # 将 debug_port 和 handler_info 合并为一个完整的配置字典
#             config = {
#                 'debug_port': debug_port,
#                 'platform_name': handler_info['platform_name'],
#                 'start_url': handler_info['start_url'],
#                 # 可以在这里添加更多配置项
#             }
#             try:
#                 obj_list.append(handler_class(config))
#             except Exception as e:
#                 raise ValueError(f"创建处理器实例时出错：{e}")
#
#     return obj_list

if __name__ == '__main__':
    pprint(platform_factory())

