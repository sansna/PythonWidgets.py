import requests
import ujson

def post_api(url, dic):
    rp = requests.post(url, json=dic)
    if rp.status_code != 200:
        return None
    elif len(rp.content) > 0:
        return ujson.loads(rp.content)
    else:
        return {}
