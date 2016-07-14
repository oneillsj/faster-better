

from xlutils.filter import process,XLRDReader,XLWTWriter
import xlrd, xlutils
from xlrd import open_workbook
from xlutils.copy import copy

import re
import argparse
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def copy2(wb):
    w = XLWTWriter()
    process(
        XLRDReader(wb,'unknown.xls'),
        w
        )
    return w.output[0][1], w.style_list

def replace_last(source_string, replace_what, replace_with):
    head, sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

# Input variables. Rack... AR switch ... DClevel cab or pod level ? console
#arg parse
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='commands')

sCab_parser = subparsers.add_parser('sCab', help='single cabinent patch plan generation')
sCab_parser.set_defaults(which='sCab')
sCab_parser.add_argument('-t', action="store", dest="tor", help='The top of rack switch hostname e.g. as-sac1-c03a')
sCab_parser.add_argument('-a', action="store", dest="agg", help='Agg layer switch hostname e.g. ar02-sac1-01 ')
sCab_parser.add_argument('-l', action="store", dest="lvl", help='DC or POD level')
sCab_parser.add_argument('-c', action="store", dest="con", help='Console router hostname e.g. co03-sac1')

args = parser.parse_args()

#generate other variables from inputs
#ms switch
print args.tor
tor_ms = args.tor
tor_ms = tor_ms.replace("as","ms")
# A-Side rack number - tor / ms / pdu rack number
a_rack = args.tor
a_rack = a_rack.split('-')
a_rack = a_rack[2]
a_rack = a_rack[:1]+'.'+a_rack[1:3]
a_rack = a_rack.upper()

# DC level agg
#print args.agg
dc_agg = args.agg
dc_agg = replace_last(dc_agg, '1', '0')

#print dc_agg

# B-Side rack number - ??? Discover?

# PDU
rack_pdu = args.tor
rack_pdu = rack_pdu.split('-')
rack_pdu = rack_pdu[2]
rack_pdu = rack_pdu.upper()
rack_pdu = "PDU-"+rack_pdu+"-A"

# Start spreadsheet magic
inBook = xlrd.open_workbook(r"PP_template.xls", formatting_info=True, on_demand=True)
inSheet = inBook.sheet_by_index(0)

# Copy the workbook, and get back the style
# information in the `xlwt` format
outBook, outStyle = copy2(inBook)

# Get the style of _the_ cell:    
xf_index = inSheet.cell_xf_index(0, 0)
saved_style = outStyle[xf_index]

# Update the cell, using the saved style as third argument of `write`:
# Update F(5) Colum with names
outBook.get_sheet(1).write(2, 5, args.tor+'-lc0')
outBook.get_sheet(1).write(3, 5, args.tor+'-lc1')
outBook.get_sheet(1).write(4, 5, args.tor+'-lc0')
outBook.get_sheet(1).write(5, 5, args.tor+'-lc1')
outBook.get_sheet(1).write(6, 5, tor_ms)
outBook.get_sheet(1).write(7, 5, tor_ms)
outBook.get_sheet(1).write(8, 5, args.tor+'-lc0')
outBook.get_sheet(1).write(9, 5, args.tor+'-lc1')
outBook.get_sheet(1).write(10,5, tor_ms)
outBook.get_sheet(1).write(11,5, args.tor+'-lc0')
outBook.get_sheet(1).write(12,5, args.tor+'-lc1')
outBook.get_sheet(1).write(13,5, rack_pdu)
outBook.get_sheet(1).write(14,5, rack_pdu)

# Update G(6) Column with correct rack (a-side rack)
outBook.get_sheet(1).write(2, 6, a_rack)
outBook.get_sheet(1).write(3, 6, a_rack)
outBook.get_sheet(1).write(4, 6, a_rack)
outBook.get_sheet(1).write(5, 6, a_rack)
outBook.get_sheet(1).write(6, 6, a_rack)
outBook.get_sheet(1).write(7, 6, a_rack)
outBook.get_sheet(1).write(8, 6, a_rack)
outBook.get_sheet(1).write(9, 6, a_rack)
outBook.get_sheet(1).write(10,6, a_rack)
outBook.get_sheet(1).write(11,6, a_rack)
outBook.get_sheet(1).write(12,6, a_rack)
outBook.get_sheet(1).write(13,6, a_rack)
outBook.get_sheet(1).write(14,6, a_rack)

# Update I(8) column with correct RU number
#outBook.get_sheet(1).write(2, 8, "blank")
#outBook.get_sheet(1).write(3, 8, "blank")
#outBook.get_sheet(1).write(4, 8, "blank")
#outBook.get_sheet(1).write(5, 8, "blank")
#outBook.get_sheet(1).write(6, 8, "blank")
#outBook.get_sheet(1).write(7, 8, "blank")
#outBook.get_sheet(1).write(8, 8, "blank")
#outBook.get_sheet(1).write(9, 8, "blank")
#outBook.get_sheet(1).write(10,8, "blank")
#outBook.get_sheet(1).write(11,8, "blank")
#outBook.get_sheet(1).write(12,8, "blank")
#outBook.get_sheet(1).write(13,8, "blank")
#outBook.get_sheet(1).write(14,8, "blank")

# Update J(9)  ... Port numbers ? 
#outBook.get_sheet(1).write(2, 9, "blank")
#outBook.get_sheet(1).write(3, 9, "blank")
#outBook.get_sheet(1).write(4, 9, "blank")
#outBook.get_sheet(1).write(5, 9, "blank")
#outBook.get_sheet(1).write(6, 9, "blank")
#outBook.get_sheet(1).write(7, 9, "blank")
#outBook.get_sheet(1).write(8, 9, "blank")
#outBook.get_sheet(1).write(9, 9, "blank")
#outBook.get_sheet(1).write(10,9, "blank")
#outBook.get_sheet(1).write(11,9, "blank")
#outBook.get_sheet(1).write(12,9, "blank")
#outBook.get_sheet(1).write(13,9, "blank")
#outBook.get_sheet(1).write(14,9, "blank")

# Update K(10) column with AR host name (only first few rows)
outBook.get_sheet(1).write(2, 10, args.agg+'-lc0')
outBook.get_sheet(1).write(3, 10, args.agg+'-lc0')
outBook.get_sheet(1).write(4, 10, args.agg+'-lc1')
outBook.get_sheet(1).write(5, 10, args.agg+'-lc1')
outBook.get_sheet(1).write(6, 10, dc_agg+'-lc0')
outBook.get_sheet(1).write(7, 10, dc_agg+'-lc1')
outBook.get_sheet(1).write(8, 10, tor_ms)
outBook.get_sheet(1).write(9, 10, tor_ms)
outBook.get_sheet(1).write(10,10, args.con)
outBook.get_sheet(1).write(11,10, args.con)
outBook.get_sheet(1).write(12,10, args.con)
outBook.get_sheet(1).write(13,10, args.con)
outBook.get_sheet(1).write(14,10, tor_ms)

print a_rack
# Update L(11) AR rack...  and our rack
outBook.get_sheet(1).write(2, 11, "blank")
outBook.get_sheet(1).write(3, 11, "blank")
outBook.get_sheet(1).write(4, 11, "blank")
outBook.get_sheet(1).write(5, 11, "blank")
outBook.get_sheet(1).write(6, 11, "blank")
outBook.get_sheet(1).write(7, 11, "blank")
outBook.get_sheet(1).write(8, 11, a_rack)
outBook.get_sheet(1).write(9, 11, a_rack)
outBook.get_sheet(1).write(10,11, "blank")
outBook.get_sheet(1).write(11,11, "blank")
outBook.get_sheet(1).write(12,11, "blank")
outBook.get_sheet(1).write(13,11, "blank")
outBook.get_sheet(1).write(14,11, a_rack)


# Update N(13) with RU positions
#outBook.get_sheet(1).write(2, 13, "blank")
#outBook.get_sheet(1).write(3, 13, "blank")
#outBook.get_sheet(1).write(4, 13, "blank")
#outBook.get_sheet(1).write(5, 13, "blank")
#outBook.get_sheet(1).write(6, 13, "blank")
#outBook.get_sheet(1).write(7, 13, "blank")
#outBook.get_sheet(1).write(8, 13, "blank")
#outBook.get_sheet(1).write(9, 13, "blank")
#outBook.get_sheet(1).write(10,13, "blank")
#outBook.get_sheet(1).write(11,13, "blank")
#outBook.get_sheet(1).write(12,13, "blank")
#outBook.get_sheet(1).write(13,13, "blank")
#outBook.get_sheet(1).write(14,13, "blank")

# Update O(14) Column... Port numbers....
outBook.get_sheet(1).write(2, 14, "xe-")
outBook.get_sheet(1).write(3, 14, "xe-")
outBook.get_sheet(1).write(4, 14, "xe-")
outBook.get_sheet(1).write(5, 14, "xe-")
outBook.get_sheet(1).write(6, 14, "ge-")
outBook.get_sheet(1).write(7, 14, "ge-")
outBook.get_sheet(1).write(8, 14, "ge-0/0/46")
outBook.get_sheet(1).write(9, 14, "ge-0/0/47")
outBook.get_sheet(1).write(10,14, "blank")
outBook.get_sheet(1).write(11,14, "blank")
outBook.get_sheet(1).write(12,14, "blank")
outBook.get_sheet(1).write(13,14, "blank")
outBook.get_sheet(1).write(14,14, "ge-0/0/0")

print "saved format_output.xls"
outBook.save(r"format_output.xls")