import os

import redis


def create_redis_connection():
    redis_host = os.environ['REDIS_CACHE_HOST']
    redis_port = os.environ['REDIS_CACHE_PORT']
    redisCache = redis.Redis(host=redis_host, port=redis_port)
    return redisCache
