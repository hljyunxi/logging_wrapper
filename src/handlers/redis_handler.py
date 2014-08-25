#!/usr/bin/env python
#coding: utf8

import logging
import redis

class RedisHandler(logging.Handler):
    """
    publish message to redis
    """
    def __init__(self, channel, host="127.0.0.1", port=6379, password=None,\
            level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.channel = channel
        self._redis_client = redis.Redis(host=host, port=port, password=password)

    def emit(self, record):
        try:
            self._redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            pass
