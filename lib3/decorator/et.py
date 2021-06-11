#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 11:37:43 PM

#import os
#import sys 
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time

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

def et(f):
    def func_wrapper(*args, **kwargs):
        st = time.time()
        ret = f(*args, **kwargs)
        et = time.time()
        print (f.__name__,et-st)
        return ret
    return func_wrapper

def et2(f):
    def func_wrapper(*args, **kwargs):
        st = time.time()
        ret, ret2 = f(*args, **kwargs)
        et = time.time()
        print (f.__name__,et-st)
        return ret, ret2
    return func_wrapper

@et
def x():
    y = 1
    for i in range(1, 200):
        y*=i
    return y

@et2
def y():
    return 1,2

def main():
    x(), y()

if __name__ == "__main__":
    main()

