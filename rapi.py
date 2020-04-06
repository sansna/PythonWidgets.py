import requests
import ujson
import time

def post_api(url, dic):
    rp = requests.post(url, json=dic)
    if rp.status_code != 200:
        return None
    elif len(rp.content) > 0:
        return ujson.loads(rp.content)
    else:
        return {}

def mpost_api_test(url, dic):
    # Same tcp conn requests, quicker
    now = time.time()
    with requests.Session() as s:
        for i in xrange(1,100):
            s.post(url, json=dic).content
    end = time.time()
    print end-now

    # Diff session request, 2x slower
    now = time.time()
    for i in xrange(1,100):
        requests.post(url, json=dic)
    end = time.time()
    print end-now
