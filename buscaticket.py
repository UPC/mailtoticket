#!/usr/bin/python
from soa.tiquets import GestioTiquets
import sys

if len(sys.argv)<2:
  print "Has de posar un id de ticket com a parametre"
  sys.exit()

id=sys.argv[1]
tiquets=GestioTiquets()
dades=tiquets.consulta_tiquet(id)
print dades
