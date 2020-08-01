#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 17:42:43

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
from lib.decorator.safe_run import safe_run_wrap

from flask import Flask
from flask import request
app = Flask(__name__)

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
def AddPath(path, f, methods=["POST"]):
    if len(path) == 0:
        return
    if path[0] != "/":
        path = "/"+path

    @app.route(path, methods=methods)
    @safe_run_wrap
    def run():
        ret = f(request.get_json(force=True))
        return ret

@safe_run_wrap
def Run(port):
    if type(port) != int:
        return
    app.run(port=port)

def main():

    def func1(json):
        mid = 0
        if "mid" in json:
            mid=json["mid"]
        if mid == 1:
            json["zz"] = 10
        return json
    AddPath("hello", func1)

    Run(8080)

if __name__ == "__main__":
    main()

