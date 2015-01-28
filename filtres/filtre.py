import hashlib
import base64
import re
import settings

import logging
logger = logging.getLogger(__name__)

class Filtre:

  def __init__(self,msg,tickets,ldap):
    self.msg=msg
    self.tickets=tickets
    self.ldap=ldap

  def es_aplicable(self):
    return False

  def filtrar(self):
    return

  def afegir_attachments(self,ticket_id,username):
    logger.info("Tractem attachments del ticket %s" % ticket_id)
    i=0;
    for a in self.msg.get_attachments():
      ctype=a.get_content_type()
      fitxer=a.get_filename()
      i+=1
      if fitxer==None:
        fitxer='attach%d.%s' % (i,ctype.split("/")[1])
      logger.info("Afegim attachment: %s" % fitxer)
      self.tickets.annexar_fitxer_tiquet(ticket_id,username,fitxer,a.get_payload())
