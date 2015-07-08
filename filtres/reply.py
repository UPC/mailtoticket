import re
import time
from filtres.filtre import Filtre
import settings

import logging
logger = logging.getLogger(__name__)

class FiltreReply(Filtre):

  solicitant=None
  ticket_id=None
  regex_reply=settings.get("regex_reply")
  regex_privat=settings.get("regex_privat")
  privat=False

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

      intern=re.compile(self.regex_privat)
      if intern.match(subject):
        logger.info ("El comentari es privat");
        self.privat=True    


      # Mirem si es un ticket valid
      ticket=self.tickets.consulta_tiquet(codi=self.ticket_id)

      # Mirem qui ha creat el ticket
      self.solicitant_segons_ticket=ticket['solicitant']
      self.solicitant=self.solicitant_segons_ticket
      logger.info ("Ticket de %s" % self.solicitant);
      logger.info ("Mail de %s" % self.msg.get_from());

      self.solicitant_segons_mail=self.get_uid()
      logger.info ("Solicitant segons Mail %s" % self.solicitant_segons_mail);

      # Si no trobem el mail, suposarem que es de qui l'ha creat
      if self.solicitant_segons_mail!=None:
        self.solicitant=self.solicitant_segons_mail
      logger.info ("Crearem comentari a nom de %s" % self.solicitant);
      return True

    except Exception, e:
      logger.info ("Peta el filtre... %s" % str(e));
      return False

  def filtrar(self):
    body=self.msg.get_body()
    if self.solicitant_segons_mail==self.solicitant_segons_ticket:
      notificat='N'
    else:
      notificat='S'
    resultat=self.tickets.afegir_comentari_tiquet(
      codiTiquet=self.ticket_id,
      usuari=self.solicitant, 
      descripcio=("[Comentari afegit des del correu de %s del %s a les %s]<br><br>" % 
	    (self.msg.get_from(),time.strftime("%d/%m/%Y"),time.strftime("%H:%M"))
		) +body,
      tipusComentari='COMENT_TIQUET_PRIVAT' if self.privat else 'COMENT_TIQUET_PUBLIC',
      esNotificat=notificat if not self.privat else 'N')

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
      return False

    self.afegir_attachments(self.ticket_id,self.solicitant)

    logger.info("Comentari afegit")
    return True

