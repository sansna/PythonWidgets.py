#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 18:16:10

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from subprocess import PIPE, Popen
from lib.decorator.safe_run import safe_run_wrap

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

@safe_run_wrap
def RunShell(*args):
    """
    Usage:
    ret = RunShell("ls -alh")
    for r in ret:
      print r
    """
    script = []
    for i in list(args):
        for j in i.split(" "):
            if len(j) == 0:
                continue
            script.append(j)
    p = Popen(script, stdout=PIPE)
    ret = p.communicate()[0]
    return ret.split("\n")

def main():
    ret = RunShell("ls -l")
    print ret
    ret = RunShell("ls", "-lhtrs ")
    print ret

if __name__ == "__main__":
    main()

