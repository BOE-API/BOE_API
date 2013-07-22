__author__ = 'Carlos'
from circus import get_arbiter
import sys


if (len(sys.argv) >= 2):
    rango =  sys.argv[1]
else:
    print 'introduce un parametro'
    sys.exit()
myprogram = {"cmd": "python manage.py getXMLSinTitulo" + rango, "numprocesses": 4}
arbiter = get_arbiter([myprogram])
try:
    arbiter.start()
finally:
    arbiter.stop()