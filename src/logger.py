#!/usr/bin/env python
#coding: utf8

import datetime
import logging
import os
import sys
import traceback
import threading

from logging.config import fileConfig
from utils import util


def loggers():
    """ get list of all loggers """
    root = logging.root
    existing = root.manager.loggerDict.keys()
    return [logging.getLogger(name) for name in existing]


class Logger(object):

    LOG_LEVELS = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG
    }

    def __init__(self, cfg):
        self.cfg = cfg
        self.setup(cfg)

    def setup(self, cfg):
        if os.path.exists(cfg.logconfig):
            fileConfig(cfg.logconfig, disable_existing_loggers=False)
        else:
            raise RuntimeError("Error: log config '%s' not found" % cfg.logconfig)


    def now(self):
        """ return date in Apache Common Log Format """
        now = datetime.datetime.now()
        month = util.monthname[now.month]
        return '[%02d/%s/%04d:%02d:%02d:%02d]' % (now.day, month,
                now.year, now.hour, now.minute, now.second)

    def reopen_files(self):
        for log in loggers():
            for handler in log.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.acquire()
                    try:
                        if handler.stream:
                            handler.stream.close()
                            handler.stream = open(handler.baseFilename,
                                    handler.mode)
                    finally:
                        handler.release()

    def close_on_exec(self):
        for log in loggers():
            for handler in log.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.acquire()
                    try:
                        if handler.stream:
                            util.close_on_exec(handler.stream.fileno())
                    finally:
                        handler.release()

if __name__ == "__main__":
    from config import logging_config
    logger = Logger(logging_config)
    logger.reopen_files()
