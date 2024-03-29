#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 17:42:43

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import re

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
if __name__ == "__main__":
    import config.base
    if not config.base.Configured:
        config.base.Configured = True
        config.base.App = "lib/web/server"
        config.base.Env = config.base.ENV_PRODUCTION
        #config.base.Env = config.base.ENV_TEST

import time
from lib3.decorator.safe_run import safe_run_wrap
import logging
from lib3.lg import logger

from flask import Flask
from flask import request
import socket
app = Flask(__name__)
# Enable UTF-8 support in resp of flask
app.config['JSON_AS_ASCII'] = False

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

pathre = re.compile('[^a-zA-Z0-9]')

def AddPath(path, f, methods=["POST"]):
    if len(path) == 0:
        return
    if path[0] != "/":
        path = "/"+path

    fun = path+str(methods)
    fun = pathre.sub('_', fun)

    """
    see https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
    for usage of @app.route
    """
    @app.route(path, methods=methods, endpoint=fun)
    def run(*args, **kwargs):
        """
        TODO: 针对同参数频繁请求，增加缓存
        """
        if request.method == 'POST':
            ret = f(request.get_json(force=True), args, kwargs)
            logger.info("path: %s, hostname: %s, host: %s, raddr: %s, methods: %s, params: %s"%(path, socket.gethostname(), request.host, request.remote_addr, methods, request.get_json(force=True)))
        elif request.method == 'GET':
            ret = f(None, args, kwargs)
            logger.info("path: %s, hostname: %s, host: %s, raddr: %s, methods: %s"%(path, socket.gethostname(), request.host, request.remote_addr, methods))
        return ret

@safe_run_wrap
def add_path(*args, **kwargs):
    """
    decorator of adding path for a function
    Usage:
    @add_path("path", methods=["POST","GET"])
    def func(json):
        print "ok"
    """
    path = args[0]
    if "methods" in kwargs:
        methods = kwargs["methods"]
    else:
        methods = ["POST"]
    def inner(func):
        AddPath(path, func, methods=methods)
        return func
    return inner

@safe_run_wrap
def Run(port=8888):
    if type(port) != int:
        return
    log = logging.getLogger("werkzeug")
    log.disabled = True
    app.run(host="0.0.0.0", port=port)

def main():

    @add_path("hello")
    def func1(json):
        mid = 0
        if "mid" in json:
            mid=json["mid"]
        if mid == 1:
            json["zz"] = 10
        if mid == -1:
            raise KeyError
        return json
    #AddPath("hello", func1)

    """
    curl -G 127.0.0.1:8080/xxx/123/xcv
    """
    @add_path("xxx/<idx>/<mmm>", methods=["GET"])
    def func2(json, *args, **kwargs):
        print json, args, kwargs
        variable_dict = args[1]
        # prints "123", unicode
        print variable_dict["idx"]
        # prints "xcv", unicode
        print variable_dict["mmm"]
        return {"zz":"你户"}

    Run(8080)

if __name__ == "__main__":
    main()

