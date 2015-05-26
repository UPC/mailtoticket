import hashlib
import base64
import re

import logging
logger = logging.getLogger(__name__)

class Filtre(object):

  def __init__(self,msg=None,tickets=None,ldap=None):
    self.msg=msg
    self.tickets=tickets
    self.ldap=ldap

  def set_mail(self,msg):
    self.msg=msg

  def set_tickets(self,tickets):
    self.tickets=tickets

  def set_ldap(self,ldap):
    self.ldap=ldap

  def es_aplicable(self):
    return False

  def filtrar(self):
    return
  
  def get_uid(self):
    if self.msg.get_uid() != None:
      return self.msg.get_uid()
    uid=self.ldap.obtenir_uid(self.msg.get_from())
    if uid != None:
      return uid
    if self.msg.get_reply_to() != None:
      return self.ldap.obtenir_uid(self.msg.get_reply_to())	  
    return None

  def codificar_base_64_si_cal(self,attachment):
    if attachment['Content-Transfer-Encoding']=='base64':
      return attachment.get_payload()      
    else:
      return base64.b64encode(attachment.get_payload())
      

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
      self.tickets.annexar_fitxer_tiquet(ticket_id,username,fitxer, self.codificar_base_64_si_cal(a))
