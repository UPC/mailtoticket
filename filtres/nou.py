import time
from filtres.filtre import Filtre
from settings import settings

import logging
logger = logging.getLogger(__name__)

class FiltreNou(Filtre):

  solicitant=None
  ticket_id=None
  valors_defecte=settings["valors_defecte"]
  equip_resolutor_nous=settings["equip_resolutor_nous"]

  def es_aplicable(self):
    logger.info("Filtre de Nou")
    logger.info("Tinc un mail de %s" % self.msg.get_from())
    self.solicitant=self.ldap.obtenir_uid(self.msg.get_from())

    logger.info("UID del solicitant: %s" % self.solicitant)
    return self.solicitant!=None

  def filtrar(self):
    logger.info("Aplico filtre...")
    body=self.msg.get_body()
    subject=self.msg.get_subject()
    recipient=self.msg.get_to()
    if recipient in self.valors_defecte:
      logger.info("Tinc parametres adicionals de %s" % recipient)
      parametres_addicionals=self.valors_defecte[recipient]
    else:
      logger.info("Poso equip resolutor %s" % self.equip_resolutor_nous)
      parametres_addicionals={"equipResolutor":self.equip_resolutor_nous}
    logger.info("A veure si puc crear el missatge de %s" % self.solicitant)
    resultat=self.tickets.alta_tiquet(
      assumpte=subject,
      solicitant=self.solicitant, 
      descripcio=("[Tiquet creat automaticament des de mail a %s ]<br><br>" % time.strftime("%c")) +body,
      **parametres_addicionals
      )

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
      return False
    logger.info("Ticket creat")

    ticket_id=resultat['codiTiquet']
    self.afegir_attachments(ticket_id,self.solicitant)

    return True
