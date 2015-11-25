import time
from filtres.filtre import Filtre
import settings

import logging
logger = logging.getLogger(__name__)

class FiltreNou(Filtre):

  solicitant=None
  ticket_id=None

  def es_aplicable(self):
    logger.info("Filtre de Nou")
    logger.info("Tinc un mail de %s" % self.msg.get_from())
    self.solicitant=self.get_uid()

    logger.info("UID del solicitant: %s" % self.solicitant)
    return self.solicitant!=None

  def filtrar(self):
    logger.info("Aplico filtre...")
    body=self.msg.get_body()
    subject=self.msg.get_subject()
    if len(subject)==0:
      subject="Ticket sense subject"
    recipient=self.msg.get_to()
    mail_from=self.msg.get_from()
    mail_resent_from=self.msg.get_resent_from()

    valors_defecte=settings.get("valors_defecte")
    equip_resolutor_nous=settings.get("equip_resolutor_nous")
    parametres_addicionals={"equipResolutor":equip_resolutor_nous}

    if mail_from in valors_defecte:
      logger.info("Tinc parametres adicionals per qui envia %s" % mail_from)
      parametres_addicionals=valors_defecte[mail_from]
    if mail_resent_from in valors_defecte:
      logger.info("Tinc parametres adicionals per d'on reenvio %s" % mail_resent_from)
      parametres_addicionals=valors_defecte[mail_resent_from]      
    if recipient in valors_defecte:
      logger.info("Tinc parametres adicionals per on envio %s" % recipient)
      parametres_addicionals=valors_defecte[recipient]      
    
    logger.info("Poso equip resolutor %s" % parametres_addicionals['equipResolutor'])
    logger.info("A veure si puc crear el ticket de %s" % self.solicitant)
    descripcio=("[Tiquet creat des del correu de %s del %s a les %s]<br><br>" % 
      (self.msg.get_from(),time.strftime("%d/%m/%Y"),time.strftime("%H:%M"))
    ) +body
    resultat=self.tickets.alta_tiquet(
      assumpte=subject,
      solicitant=self.solicitant, 
      descripcio=descripcio,
      **parametres_addicionals
      )

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
      return False
    logger.info("Ticket creat")	
	
    ticket_id=resultat['codiTiquet']
    descripcio=self.afegir_attachments_canviant_body(ticket_id,self.solicitant,descripcio)
    logger.info("Attachments (si n'hi ha) afegits")
	  
    if self.msg.get_reply_to()!=None:
      from_or_reply_to=self.msg.get_reply_to()
    else:
      from_or_reply_to=self.msg.get_from()

    if settings.get("assignar_data_resolucio_amb_data_creacio"):
      data_resolucio=time.strftime("%d-%m-%Y")
    else:
      data_resolucio=''

    resultat=self.tickets.modificar_tiquet(
      codiTiquet=ticket_id,
      emailSolicitant=from_or_reply_to,
      descripcio=descripcio,
      dataResol=data_resolucio
      )	

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
    else: 
      logger.info("Mail modificat a %s" % self.msg.get_from())

    return True