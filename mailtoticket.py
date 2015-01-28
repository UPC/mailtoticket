#!/usr/bin/python

from mailticket import MailTicket
from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
import settings
import sys

import logging
logger = logging.getLogger(__name__)

def tractament(mail):
  logger.info("Entro a mailtoticket"+mail.get_subject())

  tickets=GestioTiquets()
  ldap=GestioLDAP()

  filtres=[]
  for filtre in settings.filtres:
    filtres.append(filtre)
    filtre.set_mail(mail)
    filtre.set_tickets(tickets)
    filtre.set_ldap(ldap)
  logger.debug("Vaig a provar filtres %s" % str(filtres))


  tractat=False
  for filtre in filtres:
    logger.debug("Provo un filtre")
    if filtre.es_aplicable():
      logger.debug("Aplico filtre")
      tractat=filtre.filtrar()
      if not tractat:
        logger.info("Error al aplicar el filtre. Ho deixem correr")
        break
      # Aixo es perque el mailfilter sapiga que hem filtrat
      print "x-mailtoticket: afd25dad494b9345fa2e0a34dc2aa4c11594c3e7b672f772a7fa003ad80bd09f045a170213ae2ba4f47eb8043ac61a56e44ff031a014b82f7508bc5543960138"
      logger.info("Ja he fet el que havia de fer. Surto!")
      break
  if not tractat:
    logger.info("No he tractat el mail %s" % msg.get_subject())

if __name__ == '__main__':
  logging.basicConfig(filename=settings.log_file,level=settings.log_level)
  mail = MailTicket(sys.stdin)
  try:
    tractament(mail)
  finally:
    print mail


























