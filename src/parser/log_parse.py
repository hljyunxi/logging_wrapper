#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import time

def tailf(file_name):
    """\brief implement tail -f
    """
    with open(file_name) as f:
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line


