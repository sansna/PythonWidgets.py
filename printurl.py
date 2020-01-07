# Usage: mitmproxy -q -s printurl.py -r dumpfile
from mitmproxy import http
def request(flow: http.HTTPFlow):
    print (flow.request.url)
