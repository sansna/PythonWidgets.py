# Usage: mitmdump -q -s printurl.py -r dumpfile
from mitmproxy import http
def request(flow: http.HTTPFlow):
    if len(flow.request.content) > 0:
        #flow.request.content is of type bytes
        print ("curl -d '%s' %s?sign="%(str(flow.request.content, "utf-8"), str(flow.request.url).split("?")[0]))
