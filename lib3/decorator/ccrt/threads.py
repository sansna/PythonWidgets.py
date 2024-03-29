#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 11:01:36 PM

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import threading
from et import et

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

def tpyrun(f):
    """
    Using this decorator to thread simultaneously.
    Writing file/db/cache should be locked.
    """
    def func_wrapper(*args, **kwargs):
        t = threading.Thread(target=f,args=args, kwargs=kwargs)
        t.start()
        #t.join()
    return func_wrapper

def main():
    @tpyrun
    def run():
        time.sleep(1)
        print (1)
    @et
    def x():
        for i in range(1,10):
            run()

    x()

if __name__ == "__main__":
    main()

