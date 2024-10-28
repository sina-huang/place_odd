import threading
import time
import redis

REDIS = {
    "host": "127.0.0.1",
    "port": 6379,
}

redis_client = redis.Redis(host=REDIS["host"], port=REDIS["port"], db=0, decode_responses=True)

def publish_message():
    time.sleep(1)  # 等待一段时间以确保订阅者准备好
    redis_client.publish('channel_name', 'message_content')

def subscribe_messages():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('channel_name')
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"收到消息: {message['data']}")

# 使用线程来同时进行发布和订阅
if __name__ == "__main__":
    subscriber_thread = threading.Thread(target=subscribe_messages)
    publisher_thread = threading.Thread(target=publish_message)

    subscriber_thread.start()
    publisher_thread.start()

    subscriber_thread.join()
    publisher_thread.join()
