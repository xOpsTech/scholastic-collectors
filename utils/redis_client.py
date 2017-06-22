import redis
import json

key = 'alerts'


class RedisClient(object):
    def __init__(self, host, port):
        self.redis_client = redis.StrictRedis(host, int(port), db=0)

    def send_message(self, message):
        self.redis_client.rpush(key, json.dumps(message))