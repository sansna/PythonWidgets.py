#! /usr/bin/python3
import xlrd
from datetime import datetime
book = xlrd.open_workbook("buf.xlsx")
print(book)
sh = book.sheet_by_index(0)
f = open('buf.csv','w')
for rx in range(sh.nrows):
    for cx in range(sh.ncols):
        if cx != 0:
            f.write(",")
        if rx != 0 and (cx == 2 or cx == 3):
            f.write('{}'.format(datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx,cx),book.datemode))))
            continue
        f.write('{}'.format(sh.cell_value(rx,cx)))
    if rx != sh.nrows:
        f.write("\n")

f.close()
