import json

def parse_ws_message(data):
    try:
        message_dict = json.loads(data)
        data_str = message_dict['message']
        if isinstance(data_str, str):
            data_dict = json.loads(data_str)
        elif isinstance(data_str, dict):
            data_dict = data_str
        return data_dict
    except json.JSONDecodeError as e:
        print('ws解析错误')
        return None