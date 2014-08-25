#!/usr/bin/env python
#coding: utf8

import logging
import redis

class RedisHandler(logging.Handler):
    """
    publish message to redis
    """
    @classmethod
    def to(cls, channel, host="127.0.0.1", port=6379,\
            password=None, level=logging.DEBUG):
        return cls(channel, redis.Redis(host=host, port=port, password=password),\
                level=level)

    def __init__(self, channel, redis_client, level):
        loggin.Handler.__init__(self, level)
        self.channel = channel
        self._redis_client = redis_client

    def emit(self, record):
        try:
            self._redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            pass
