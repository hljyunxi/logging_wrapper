#!/usr/bin/env python
#coding: utf8

import re
import logging

try:
    from collections import OrderedDict
except ImportError:
    pass

RESERVED_ATTRS = (
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module',
    'msecs', 'message', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'thread', 'threadName'
)

RESERVED_ATTRS_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))

class JsonFormater(logging.formater):
    def __init__(self, *largs, **kwargs):
        self._json_encoder = kwargs.pop('json_encoder', None)
        self._json_default = kwargs.pop('json_default', None)
        super(JsonFormater).__init__(*largs, **kwargs)

    @property
    def json_encoder(self):
        def _default_json_handler(obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime(self.datefmt or '%Y-%m-%dT%H:%M')
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            elif isinstance(obj, datetime.time):
                return obj.strftime('%H:%M')
            return str(obj)

        return self._json_encoder or _default_json_handler

    @property
    def required_fields(self):
        if not hasattr(self, '_required_fields'):
            standard_formaters = re.compile(r'\(.+?\)', re.IGNORECASE)
            self._required_fields = standard_formaters.findall(self._fmt)
            
        return self._required_fields

    @property
    def skipped_fields(self):
        if not hasattr(self, '_skipped_fields'):
            self._skipped_fields = dict(self._required.items() + \
                    RESERVED_ATTRS_HASH.items())

        return self._skipped_fields

    def merge_record_extra(self, out, record):
        for k, v in record.__dict__.iteritems():
            if not k in (self.required_fields+self.skipped_fields) and\
                    not k.startswith('_'):
               out[k] = v

    def format(self, record):
        extras = {}
        if isinstance(record.msg, dict):
            extras = record.msg

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        for k in self.required_fields:
            log_record[k] = record.__dict__.get(k)

        log_record.update(extras)
        self.merge_record_extra(log_record, record)
        
        return json.dumps(log_record, cls=self.json_encoder)


class JsonStringFormater(JsonFormater):
    """\brief return formatted string
    """
    def format(self, record):
        extras = {}
        if isinstance(record.msg, dict):
            extras = record.msg

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        for k in self.required_fields:
            log_record[k] = record.__dict__.get(k)

        log_record.update(extras)
        self.merge_record_extra(log_record, record)
        
        return self._fmt % log_record
