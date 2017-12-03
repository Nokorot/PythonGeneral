#! usr/bin/python

import sys, os

from jlybuilder import JLYFrame

frame = JLYFrame(os.path.abspath(sys.argv[1]))
frame.build()
frame.open()
