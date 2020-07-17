# Usage: mitmdump -q -s printurl.py -r dumpfile
from mitmproxy import http
def request(flow: http.HTTPFlow):
    if len(flow.request.content) > 0:
        #flow.request.content is of type bytes
        # others like str(flow.response.content, "utf-8")
        # flow.request.headers
        # flow.reqhest.method, flow.request.path
        # More see: https://mitmproxy.readthedocs.io/en/v2.0.2/scripting/api.html#mitmproxy.http.HTTPRequest
        print ("curl -d '%s' %s?sign="%(str(flow.request.content, "utf-8"), str(flow.request.url).split("?")[0]))
        print (flow.request.path)
