'''record clicks

Usage:
    clicker.py (--logfile=<logfile>)

Options:
    --logfile=<logfile>         filename
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This script is an modification of the script below.
#

#
# examples/record_demo.py -- demonstrate record extension
#
#    Copyright (C) 2006 Alex Badea <vamposdecampos@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Simple demo for the RECORD extension
# Not very much unlike the xmacrorec2 program in the xmacro package.

# Original source code (examples/recode_demo.py) is available at:
#   The Python X Library
#   http://python-xlib.sourceforge.net/


import sys
import os

import glob
import logging
import logging.handlers

import datetime as dt

from docopt import docopt

########################
#LOG_FILENAME = 'clicks.log'
MAX_FILE_SIZE = 5000000
BACKUP_COUNT = 20
COMPRESS = ('bzip2','.bz2')

arguments = docopt(__doc__, version='clicker')
LOG_FILENAME = arguments['--logfile']

############
class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0, compress=('true', '')):
        logging.handlers.RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)
        self.compress = compress

    def doRollover(self):
        self.stream.close()
        os.system('wc %s' % self.baseFilename)
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d%s" % (self.baseFilename, i,     self.compress[1])
                dfn = "%s.%d%s" % (self.baseFilename, i + 1, self.compress[1])
                if os.path.exists(sfn):
                    #print "%s -> %s" % (sfn, dfn)
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn  = self.baseFilename + ".1"
            dfnz = self.baseFilename + ".1" + self.compress[1]
            if os.path.exists(dfnz):
                os.remove(dfnz)
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)
            os.system('%s %s' % (self.compress[0], dfn))
            #print "%s -> %s" % (self.baseFilename, dfn)
        self.mode = 'w'
        self.stream = self._open()

class MyFormatter(logging.Formatter):
    converter=dt.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


# Set up a specific logger with our desired output level
my_logger = logging.getLogger('KeyLogger')
my_logger.setLevel(logging.INFO)

# Add the log message handler to the logger
handler = CompressedRotatingFileHandler(
              LOG_FILENAME, maxBytes=MAX_FILE_SIZE, backupCount=BACKUP_COUNT, compress=COMPRESS)
#handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
handler.setFormatter(MyFormatter("%(asctime)s;%(message)s", "%s.%f"))
my_logger.addHandler(handler)


from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

local_dpy = display.Display()
record_dpy = display.Display()

def lookup_keysym(keysym):
    for name in dir(XK):
        if name[:3] == "XK_" and getattr(XK, name) == keysym:
            return name[3:]
    return "[%d]" % keysym

def record_callback(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        print "* received swapped protocol data, cowardly ignored"
        return
    if not len(reply.data) or ord(reply.data[0]) < 2:
        # not an event
        return

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)

        if event.type in [X.KeyPress, X.KeyRelease]:
            pr = event.type == X.KeyPress and "Press" or "Release"

            keysym = local_dpy.keycode_to_keysym(event.detail, 0)
            if not keysym:
                my_logger.info("KeyCode %s %s" % (pr, event.detail))
            else:
                #my_logger.info("keystr %s %s" % (pr, lookup_keysym(keysym)))
                my_logger.info("%s" % (lookup_keysym(keysym)))

            # quit on escape
            #if event.type == X.KeyPress and keysym == XK.XK_Escape:
            #    local_dpy.record_disable_context(ctx)
            #    local_dpy.flush()
            #    return

# Check if the extension is present
if not record_dpy.has_extension("RECORD"):
    print "RECORD extension not found"
    sys.exit(1)
r = record_dpy.record_get_version(0, 0)

#print "RECORD extension version %d.%d" % (r.major_version, r.minor_version)
print "-----------------------"
print "Tio Tor  #   #  Tor Tio"
print " e   r  <#> <#>  u   i "
print "-----------------------"
print "Abw 3er 5er 5er 3er Abw"
print " d   f   g   h   j   k "
print "-----------------------"
print "Aus Set ext "
print "spc rtr C+c "
print "-----------------------"
print ""



# Create a recording context; we only want key and mouse events
ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyPress),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

# Enable the context; this only returns after a call to record_disable_context,
# while calling the callback function in the meantime
record_dpy.record_enable_context(ctx, record_callback)

# Finally free the context
record_dpy.record_free_context(ctx)

