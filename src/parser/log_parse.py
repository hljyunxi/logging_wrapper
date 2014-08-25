#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import time
import re

REGEX_SPECIAL_CHARS = r'([\.\*\+\?\|\(\)\{\}\[\]])'
REGEX_LOG_FORMAT_VARIABLE = r'%([a-z0-9\_]+)[dsf]'

def tailf(file_name):
    """\brief implement tail -f
    """
    with open(file_name) as f:
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line


def build_pattern(log_format):
    pattern = re.sub(REGEX_SPECIAL_CHARS, r"\\\1", log_format)
    pattern = re.sub(REGEX_LOG_FORMAT_VARIABLE, "(?P<\\1>.*)", pattern)
    return pattern


def extract_variables(log_format):
    for match in re.findall(REGEX_LOG_FORMAT_VARIABLE, log_format):
        yield match


def parse_file(file_name, log_format):
    pattern = build_pattern(log_format)
    for i in tailf(file_name):
        match_obj = pattern.search(i)
        if match_obj:
            yield match_obj.groupdict()

if __name__ == "__main__":
    pass
