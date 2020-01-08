# -*- coding: UTF-8 -*-
# Note: this file is using python2, not python3

# Most important info from https://pythonhosted.org/kitchen/unicode-frustrations.html:
#+ unicodes are python formatted, str type is I/O oriented. Thus, type unicode cannot
#+ be redirected to files, only str type can be redirected to I/O devices(file etc.).

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

# Print with format, can be printed screen/file.
a=u'\u7537' # a is of type unicode
#print u"{0}".format(a)  # print in unicode way, this cannot be printed to file
print "{0}".format(a.encode("utf-8")) # print in str way

# Use this to redirect stdout to file.
# Note: after following process, stdout only accept unicode output, str typed output will panic the program.
a=u'\u7537' # a is of type unicode
import sys
import codecs
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

print a
