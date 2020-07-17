import threading
import requests

# NOTE:Each thread has different values at this space
threadlocal = threading.local()

def get_session():
    if hasattr(threadlocal, "session"):
        return threadlocal.session
    else:
        threadlocal.session = requests.Session()
        return threadlocal.session

def f(url, dic):
    print get_session().post(url, json=dic).content

def start(url, dic):
    if url == "":
        url = "http://api.iupvideo.net/config/get"
    if dic == {}:
        dic = {}
    t1 = threading.Thread(target=f,args=[url, dic])
    t2 = threading.Thread(target=f,args=[url, dic])

    t1.start()
    t2.start()

    t1.join()
    t2.join()
