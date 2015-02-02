from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
from settings import settings
from filtres.nou import FiltreNou
from filtres.reply import FiltreReply

import logging
logger = logging.getLogger(__name__)


def get_class( kls ):
  """ 
  Obtenim classe a partir del seu nom en un string
  http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname 
  """
  parts = kls.split('.')
  module = ".".join(parts[:-1])
  m = __import__( module )
  for comp in parts[1:]:
    m = getattr(m, comp)            
  return m

def aplicar_filtres(mail, tickets=None, ldap=None):
  """
  Apliquem tots els filtres segons l'ordre definit al settings, mirant primer si son aplicables i aplicant despres
  """
  logger.info("Entro a mailtoticket"+mail.get_subject())

  if tickets is None: tickets=GestioTiquets()
  if ldap is None: ldap=GestioLDAP()

  filtres=[]
  for nom_filtre in settings["filtres"]:
    classe_filtre=get_class(nom_filtre)
    filtre=classe_filtre(mail,tickets,ldap) # Aixo obte la classe i d'aqui crida al constructor
    filtres.append(filtre)

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
