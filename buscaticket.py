#!/usr/bin/python
# -*- coding: utf-8 -*-
from soa.tiquets import GestioTiquets
import sys

if len(sys.argv) < 2:
    print ("INFO: Cal indicar un codi de ticket per fer la cerca. Exemple: ./buscaticket.py 950010")
    sys.exit()

id_ticket = sys.argv[1]
tiquets = GestioTiquets()
print ("Ticket " + id_ticket + ". Obert per l'usuari: " + tiquets.username_gn6)
dades = tiquets.consulta_tiquet(id_ticket)
print (dades)
