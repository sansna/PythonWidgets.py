#!/bin/python3
# This *decorators* module resides in current dir.
from decorators import timer
from collections import *
# namedtuples/defaultdict/OrderedDict

@timer
def main():
    # ordereddict preserves orders at insertion.
    odict=OrderedDict()
    odict.update({'key1':1})
    odict.update({'key2':2})
    # iterate odict forwardly
    for k in odict:
        print(k)
    # backwardly
    for k, v in reversed(odict.items()):
        print(k,v)

    # Whenever accesses a non-exist k/v in ddict, returns dict(), also works for int()/0, float()/0.0
    ddict=defaultdict(dict)
    print(ddict['sdf'])

    # create a namedtuple named A, with attributes ordered as 2nd param
    A=namedtuple('A','count enabled color')
    # This creates a namedtuple, which count=100, enabled=True, color='red'
    z=A(100,False,'red')
    print(z, z.count)

if __name__ == '__main__':
    main()
