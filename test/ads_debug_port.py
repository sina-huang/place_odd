import requests

# ko825f2
ADS ={
    'ads_id' : "ko825f2",
    'ads_open_url' : "http://local.adspower.com:50325/api/v1/browser/start?user_id=",
    'ads_close_url' : "http://local.adspower.com:50325/api/v1/browser/stop?user_id="
}

ads_open_url = ADS['ads_open_url'] + ADS['ads_id']
resp = requests.get(ads_open_url).json()
if resp["code"] != 0:
    print(f'[ads 启动失败]，检查工厂文件配置和ads配置')
debug_port = int(resp["data"]["debug_port"])


print(debug_port)