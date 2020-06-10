# -*- coding: utf-8 -*-
#!/usr/bin/python
from soa.tiquets import GestioTiquets
import sys

if len(sys.argv) < 2:
    print ("Has de posar un id de ticket com a paràmetre.")
    sys.exit()

id_ticket = sys.argv[1]
tiquets = GestioTiquets()
print ("Username: " + tiquets.username_gn6)
dades = tiquets.consulta_tiquet(id_ticket)
print (dades)
