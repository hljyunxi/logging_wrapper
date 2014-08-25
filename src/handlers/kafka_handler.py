#!/usr/bin/env python
#coding: utf8

import logging

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, KeyedProducer

class ProducerType(object):
    SIMPLE, KEYED = range(1, 3)


class KafkaHandler(logging.Handler):
    """
    publish message to kafka
    """
    def __init__(self, topic, producer_type=ProducerType.SIMPLE,\
            host_port="127.0.0.1:9092", **producer_opts):

        self.topic = topic
        self.host_port = host_port
        if producer_type == ProducerType.SIMPLE:
            self.producer = SimpleProducer(KafkaClient(host_port),\
                    **producer_opts)
        else:
            self.producer = KeyedProducer(KafkaClient(host_port),\
                    **producer_opts)

    def emit(self, record):
        try:
            response = self.producer.send_messages(self.topic,\
                    self.format(record))
        except:
            pass
