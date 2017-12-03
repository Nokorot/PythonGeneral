from icsFormat import *

from sys import argv

if len(argv) < 3:
    print "To few argumenst"
    sys.exit()

ICS = ICSData().loadFile(argv[1])

for f in argv[2:]:
    ICS.assamble( ICSData().loadFile(f) )

ICS.writeFile("out.ics")
