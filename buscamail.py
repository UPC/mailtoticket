#!/usr/bin/python
# -*- coding: utf-8 -*-
from soa.identitat import GestioIdentitat
import sys

if len(sys.argv) < 2:
    print ("Cal posar un email com a paràmetre.")
    sys.exit()

if __name__ == '__main__':
    mail = sys.argv[1]
    identitat = GestioIdentitat()
    uid = identitat.obtenir_uid(mail)
    if uid:
        print ("El username associat al email '{}' és: {} ".format(mail, uid))
    else:
        print ("No s'ha trobat username per l'email: {}".format(mail))