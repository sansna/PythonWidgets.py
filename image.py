import requests
s = requests.Session()
r = s.get('http://tieba.baidu.com/p/2166231880')
import re
t = r.text
a=r'img pic_type="0" class=\"BDE_Image\" src=\"((https|http)://(([a-z]+\.?)+(/[a-zA-Z%0-9=]+)+).jpg)'
lista= re.findall(a,t)
while lista.__len__() !=0:
    link=lista.pop()[0]
    links=requests.Session()
    linkr=requests.get(link)
    linkf=open(str(lista.__len__())+'.jpg','wb')
    for chunk in linkr.iter_content():
        linkf.write(chunk)
    linkf.close()
