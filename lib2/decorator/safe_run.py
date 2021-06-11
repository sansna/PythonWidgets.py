#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 10:30:01 PM

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import functools
from inspect import stack
from lib.lg import logger

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

def safe_run(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return func_wrapper

def safe_run_wrap(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            logger.debug("safe_run_wrap.%s: args: %s, kwargs: %s"%(func.__name__, args, kwargs))
            return func(*args, **kwargs)
        except Exception as e:
            st = stack()
            if len(st) > 1:
                st = st[1:]
            ret_stack = []
            for s in st:
                ret_stack.append(s[1:])
            logger.error("in func: %s, err: %s, stack: %s"%(func.__name__, e, ret_stack))
            return None
    return func_wrapper

@safe_run_wrap
def main():
    print 1/0

if __name__ == "__main__":
    main()

