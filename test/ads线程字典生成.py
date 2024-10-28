# settings.py

# 平台信息
PLATFORMS = {
    'Rollbit': {
        'start_url': 'https://rollbit.com',
        'platform_name': 'Rollbit'
    },
    'Stake': {
        'start_url': 'https://stake.com',
        'platform_name': 'Stake'
    },
    # 可以添加更多平台
}

# 处理器类映射
PLATFORM_HANDLERS = {
    'Rollbit': 'RollbitHandler',
    'Stake': 'StakeHandler',
    # 可以添加更多平台
}

# ads_id 列表
ADS_IDS = ['knbvol0', 'ko825f2']
from pprint import pprint


# 构建配置字典
a = {}
for ads_id in ADS_IDS:
    a[ads_id] = {}
    for platform_name, platform_info in PLATFORMS.items():
        handler_class = PLATFORM_HANDLERS[platform_name]
        a[ads_id][platform_name] = {
            'class': handler_class,
            'info': platform_info
        }
pprint(a)
