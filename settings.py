
ADS_ID = ['knbvol0','ko825f2']


ADS ={
    'ads_id' : "knbvol0",
    'ads_open_url' : "http://local.adspower.com:50325/api/v1/browser/start?user_id=",
    'ads_close_url' : "http://local.adspower.com:50325/api/v1/browser/stop?user_id="
}

WS ={
    'url_betting' : "ws://192.166.82.38:8000/ws/betting/"
}

Platform ={
    'Stake': {
        'platform_name' : 'Stake',
        'start_url' : 'https://stake.com/zh/sports/live/soccer',
    },
    'Rollbit': {
        'platform_name' : 'Rollbit',
        'start_url' : 'https://rollbit.com/sports?bt-path=%2Fsoccer-1',
    },
    # 'Sportbet': {
    #     'platform_name' : 'Sportbet',
    #     'start_url' : 'https://sportsbet.io/zh/sports/soccer/inplay',
    # }
}


REDIS= {
    "host": "127.0.0.1",
    "port": 6379,
}




