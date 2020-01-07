# -*- coding: UTF-8 -*-
# This can only be printed on screen, but not into file.
#a='\u7537' # a is of type string
#print a.decode('unicode-escape')

a='男' # a is of type string
# This can be printed both on screen/file.
#print a
# decode the string to unicode with unicode()
s = unicode(a,'utf-8') # now s = u'\u7537', of type unicode
# This can be printed on screen, but not into file.
#print s
# This can be printed both on screen/file.
print s.encode('utf-8')

# This can be printed into file.
a=u'\u7537' # a is of type unicode
a=a.encode('utf-8')
print a

# Use this to redirect stdout to file.
a=u'\u7537' # a is of type unicode
import sys
import codecs
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

print a
