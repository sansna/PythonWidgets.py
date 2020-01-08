# -*- coding: utf-8 -*-
def to_str(thing):
    if type(thing) is str:
        return thing
    elif type(thing) is unicode:
        return thing.encode("utf-8")
    elif type(thing) is int:
        return str(thing)
    elif type(thing) is float:
        return str(thing)

def to_unicode(thing):
    if type(thing) is unicode:
        return thing
    elif type(thing) is str:
        return unicode(thing, "utf-8")
    elif type(thing) is int:
        return unicode(thing)
    elif type(thing) is float:
        return unicode(thing)
