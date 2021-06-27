#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 17:32:31

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import yagmail as yg
from lib3.decorator.safe_run import safe_run_wrap

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
def InitUser(user, pw, host='smtp.exmail.qq.com'):
    # QQ mail example
    a=yg.SMTP(user=user,password=pw,host=host)
    return a

@safe_run_wrap
def SendAsUser(obj,to,sub,att):
    """
    obj: user, from obj = InitUser()
    to: "mail"
    sub: "My sub"
    att: ["file1", "file2"], some server may check total size/ file numbers
    """
    obj.send(to, subject=sub, attachments=att)

@safe_run_wrap
def SendAsUserCont(obj, to, sub, cont, att):
    """
    cont: str. mail content
    """
    obj.send(to, subject=sub, attachments=att, contents=cont)

def main():
    user = InitUser()
    SendAsUser(user, "1@qq.com", "Hello world!", ["file.txt"])

if __name__ == "__main__":
    main()

