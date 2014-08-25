#!/usr/bin/env python
#coding: utf8

import datetime
import logging
import os
import sys
import traceback
import threading

from logging.config import fileConfig


CONFIG_DEFAULTS = dict(
        version = 1,
        disable_existing_loggers = False,

        loggers = {
            "root": { "level": "INFO", "handlers": ["console"] },
            "error": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": True,
                "qualname": "gunicorn.error"
            }
        },
        handlers = {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": "sys.stdout"
            }
        },
        formatters = {
            "generic": {
                "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "class": "logging.Formatter"
            }
        }
)

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
        self.error_handlers = []
        self.access_handlers = []
        self.cfg = cfg
        self.setup(cfg)

    def setup(self, cfg):
        if os.path.exists(cfg.logconfig):
            fileConfig(cfg.logconfig, defaults=CONFIG_DEFAULTS,
                    disable_existing_loggers=False)
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
