import sys
import json
import signal
import redis
import logging as log

log.basicConfig(filename="log.txt", format="%(asctime)s: %(filename)s:%(lineno)s: %(funcName)s %(levelname)s: %(message)s", level=log.INFO)

#def sigterm_handler(_signo, _stack_frame):
#    sys.exit(0)
#
#signal.signal(signal.SIGTERM, sigterm_handler)

def main():
    c = redis.StrictRedis(host="127.0.0.1",port=6379,password="")
    while True:
        try:
            c.lpush("wwoww", "asdfsadf")
            ret=c.brpop("wwoww", timeout=0)
            print(str(ret[1]))
        except Exception as e:
            log.info("%s"%e)

if __name__ == "__main__":
    main()
