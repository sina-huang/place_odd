# config.py
import time

import requests
from pprint import pprint
from settings import ADS_ID, ADS, WS, Platform, REDIS
# 导入平台处理器类
from platform_handlers.rollbit_handler import RollbitHandler
from platform_handlers.stake_handler import StakeHandler


# 创建平台名称与处理器类的映射
PLATFORM_HANDLERS = {
    'Stake': StakeHandler,
    'Rollbit': RollbitHandler,
    # 'Sportbet': SportbetHandler,
    # 添加其他平台处理器类
}


def get_platform_configs():
    platform_configs = {}
    for ads_id in ADS_ID:
        # 启动 ads 浏览器，获取 debug_port
        ads_open_url = ADS['ads_open_url'] + ads_id
        resp = requests.get(ads_open_url).json()
        time.sleep(2)
        if resp["code"] != 0:
            print(f'[ads 启动失败] ads_id: {ads_id},处理办法: 需要取配置两个ads浏览器请求直接的时间间隔，如果间隔太短，ads浏览器会启动失败')
            continue
        debug_port = int(resp["data"]["debug_port"])

        # 以 debug_port 作为键
        platform_configs[debug_port] = {}
        for platform_name, platform_info in Platform.items():
            handler_class = PLATFORM_HANDLERS.get(platform_name)
            if handler_class:
                platform_configs[debug_port][platform_name] = {
                    'class': handler_class,
                    'platform_name': platform_info['platform_name'],
                    'start_url': platform_info['start_url']
                }
            else:
                raise ValueError(f"未找到平台处理器：{platform_name}")
    return platform_configs






# 在其他模块中，您可以通过调用 get_platform_configs() 来获取配置字典


if __name__ == '__main__':
    pprint(get_platform_configs())