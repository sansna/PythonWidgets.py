import yagmail as yg
import argparse

def init():
    # QQ mail example
    a=yg.SMTP(user='',password='',host='smtp.exmail.qq.com')
    return a

def send(obj,to,sub,att):
    obj.send(to, subject=sub, attachments=att)

def main():
    p = argparse.ArgumentParser(conflict_handler='resolve')
    p.add_argument("-s", type=str, help="subject")
    # list()
    p.add_argument("-a", action="append", help="attachments")
    # list()
    p.add_argument("-t", action="append", default=[""], help="target mail addr")
    args = p.parse_args()
    y=init()
    send(y,args.t, args.s, args.a)

if __name__ == '__main__':
    main()
