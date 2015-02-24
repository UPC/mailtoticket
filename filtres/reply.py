import re
import time
from filtres.filtre import Filtre
from settings import settings

import logging
logger = logging.getLogger(__name__)

class FiltreReply(Filtre):

  solicitant=None
  ticket_id=None
  regex_reply=settings["regex_reply"]

  def es_aplicable(self):
    logger.info("Filtre de reply");

    try:
      # Ara anem a veure que podem fer amb aquest missatge
      subject = self.msg.get_subject_ascii()
      logger.info ("Buscant numero a  %s" % subject);
      p=re.compile(self.regex_reply)
      m = p.match(subject)
      self.ticket_id=m.group(1)

      logger.info ("Trobat ticket %s" % self.ticket_id);

      # Mirem si es un ticket valid
      ticket=self.tickets.consulta_tiquet(codi=self.ticket_id)

      # Mirem qui ha creat el ticket
      self.solicitant=ticket['solicitant']
      logger.info ("Ticket de %s" % self.solicitant);
      logger.info ("Mail de %s" % self.msg.get_from());

      solicitant_segons_mail=self.get_uid()
      logger.info ("Solicitant segons Mail %s" % solicitant_segons_mail);

      # Si no trobem el mail, suposarem que es de qui l'ha creat
      if solicitant_segons_mail!=None:
        self.solicitant=solicitant_segons_mail
      logger.info ("Crearem comentari a nom de %s" % self.solicitant);
      return True

    except:
      logger.info ("Peta el filtre...");
      return False

  def filtrar(self):
    body=self.msg.get_body()
    resultat=self.tickets.afegir_comentari_tiquet(
      codiTiquet=self.ticket_id,
      usuari=self.solicitant, 
      descripcio=("[Comentari afegit automaticament des de correu de %s el %s ]<br><br>" % (self.msg.get_from(),time.strftime("%d/%m/%Y %H:M"))) +body,
      tipusComentari='COMENT_TIQUET_PUBLIC',
      esNotificat='S')

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
      return False

    self.afegir_attachments(self.ticket_id,self.solicitant)

    logger.info("Comentari afegit")
    return True

