#!/usr/bin/python

from mailticket import MailTicket
from settings import settings,load_settings
import filtres
import sys
import getopt

import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
  opts, args = getopt.getopt(sys.argv[1:], 'c:')
  for o, a in opts:
    if o=='-c': settings.load_settings(a)

  logging.basicConfig(filename=settings["log_file"],level=eval(settings["log_level"]))
  tickets=GestioTiquets()
  ldap=GestioLDAP()

  try:
    mail = MailTicket(sys.stdin)
    if filtres.aplicar_filtres(mail):
      print "x-mailtoticket: afd25dad494b9345fa2e0a34dc2aa4c11594c3e7b672f772a7fa003ad80bd09f045a170213ae2ba4f47eb8043ac61a56e44ff031a014b82f7508bc5543960138"
  finally:
    print mail