# Run this as: python argp.py 999 -m df -m 12 -d 123 23 -i 12 -d xc ksdf -+new asdf -r sz
#+ Usage of argparse: https://docs.python.org/3/library/argparse.html
import argparse

p = argparse.ArgumentParser(conflict_handler='resolve', add_help=False)
# This works
p.add_argument("-p", "--hel", "--help-menu", type=str, default="host", help="sdfsdf")
p.add_argument("-hm", type=str, default="lsdf", help="sdfsdf")
# 1 dim list: [], add args by specify another "-m"
p.add_argument("-m", action="append")
# 1 dim array, collisionable
p.add_argument("-n", nargs="+")
# another 1 dim array. extends current array each time specifies, argparse version should >=3.8
#p.add_argument("-e", action="extend")
# 2 dim list: [[], []], each "-d" specifies a list, separated by space.
#+ nargs values: '?', '*', 'N', '+'
p.add_argument("-d", action="append", nargs="*")
# specify type, may gen error.
p.add_argument("-i", type=int)
# specify choices, may gen error.
p.add_argument("-c", choices=["left", "right", "up", "down"])
# default var
p.add_argument("level", type=int)
# required, also note the first option name is used as destination variable name.
p.add_argument("--required","-r", required=True)

# Parent/Child usage, newp has all of p's arguments, and rename to WOW
newp = argparse.ArgumentParser(parents=[p], prog="WOW", prefix_chars="-+")
# Possible prefix char usage
newp.add_argument("-+new", type=str)

args = newp.parse_args()
print "hm: %s"%type(args.hm),
print args.hm
print "1 dim: m:%s"%type(args.m)
print args.m
if args.m != None:
    for i in args.m:
        print "type:%s,val:%s"%(type(i),i)
print "2-dimension:",args.d
if args.d != None:
    for i in args.d:
        if i == None:
            continue
        for j in i:
            print "type: %s, val: %s"%(type(j),j)

print "type specified:",type(args.i)
print "choices: ",args.c
print "first var: %s"%args.level
print "newp:%s"%args.new
print "required:%s"%args.required
#print "extend: %s"%args.e
print "nargs: %s"%args.n
