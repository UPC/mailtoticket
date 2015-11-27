import hashlib
import base64
import re

import logging
logger = logging.getLogger(__name__)

class Filtre(object):

  def __init__(self,msg=None,tickets=None,identitat=None):
    self.msg=msg
    self.tickets=tickets
    self.identitat=identitat

  def set_mail(self,msg):
    self.msg=msg

  def set_tickets(self,tickets):
    self.tickets=tickets

  def set_identitat(self,identitat):
    self.identitat=identitat

  def es_aplicable(self):
    return False

  def filtrar(self):
    return
  
  def get_uid(self):
    uid=self.identitat.obtenir_uid(self.msg.get_from())
    if uid != None:
      return uid
    if self.msg.get_reply_to() != None:
      return self.identitat.obtenir_uid(self.msg.get_reply_to())	  
    return None

  def codificar_base_64_si_cal(self,attachment):
    if attachment['Content-Transfer-Encoding']=='base64':
      return attachment.get_payload()      
    else:
      return base64.b64encode(attachment.get_payload())

  def afegir_attachments_canviant_body(self,ticket_id,username,body):
    (cids,ids)=self.afegir_attachments(ticket_id,username)
    body=self.tractar_attachments_inline(body,cids)
    body=self.afegir_links_attachments(body,ids)
    return body

  def afegir_attachments(self,ticket_id,username):
    logger.info("Tractem attachments del ticket %s" % ticket_id)
    i=0;
    cids={}
    ids=[]
    for a in self.msg.get_attachments():
      ctype=a.get_content_type()
      fitxer=a.get_filename()
      cid=a.get('Content-ID')
      i+=1
      if fitxer==None:
        fitxer='attach%d.%s' % (i,ctype.split("/")[1])
      logger.info("Afegim attachment: %s / %s" % (fitxer,cid))
      codi_annex=self.tickets.annexar_fitxer_tiquet(ticket_id,username,fitxer, self.codificar_base_64_si_cal(a))
      if cid!=None: 
        cids[cid[1:-1]]=codi_annex
      else:
        ids.append(codi_annex)
    return (cids,ids)

  def tractar_attachments_inline(self,html,cids):
    cids_no_substituits=[]
    for cid in cids:
      id=cids[cid]
      if cid in html:
        html=html.replace("cid:"+cid,self.url_attachment(id))
    return html

  def afegir_links_attachments(self,html,ids):
    if len(ids)==0: 
      return html
    html=html+"Attachments:<ul>"
    for id in ids:
      url=self.url_attachment(id)
      html=html+"<li><a href=\"%s\">%s</a>",(url,url)
    html=html+"</ul>"
    return html

  def url_attachment(self,id):
    return "/tiquetsusuaris/control/file?fileId=%s" % id