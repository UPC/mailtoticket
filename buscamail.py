#!/usr/bin/python
# -*- coding: utf-8 -*-
from soa.identitat import GestioIdentitat
import sys

if len(sys.argv) < 2:
    print ("INFO: Cal indicar un correu per fer la cerca. \
        Exemple: ./buscamail test@upc.edu")
    sys.exit()

if __name__ == '__main__':
    mail = sys.argv[1]
    identitat = GestioIdentitat()
    uid = identitat.obtenir_uid(mail)
    if uid:
        print ("El nom d'usuari associat al correu '{}' és: \
            {} ".format(mail, uid))
    else:
        print ("No s'ha trobat cap nom d'usuari per correu indicat: \
            {}".format(mail))
