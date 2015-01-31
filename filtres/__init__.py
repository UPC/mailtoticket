from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
from settings import settings
from filtres.nou import FiltreNou
from filtres.reply import FiltreReply

import logging
logger = logging.getLogger(__name__)

def aplicar_filtres(mail, tickets=None, ldap=None):
  logger.info("Entro a mailtoticket"+mail.get_subject())

  if tickets is None: tickets=GestioTiquets()
  if ldap is None: tickets=GestioLDAP()

  filtres=[]
#  for filtre in eval(settings["filtres"]):
#    filtres.append(filtre)
#    filtre.set_mail(mail)
#    filtre.set_tickets(tickets)
#    filtre.set_ldap(ldap)

  filtres.append(FiltreReply(mail,tickets,ldap))
  filtres.append(FiltreNou(mail,tickets,ldap))

  logger.info("Vaig a provar filtres %s" % str(filtres))


  tractat=False
  for filtre in filtres:
    logger.info("Provo un filtre")
    if filtre.es_aplicable():
      logger.info("Aplico filtre")
      tractat=filtre.filtrar()
      if tractat:
        logger.info("Ja he fet el que havia de fer. Surto!")
        return True
      else:
        logger.info("Error al aplicar el filtre. Ho deixem correr i seguim provant")

  if not tractat:
    logger.info("No he tractat el mail [%s]" % mail.get_subject())
    return False
