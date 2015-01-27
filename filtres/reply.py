import re
import time
from filtres.filtre import Filtre

import logging
logger = logging.getLogger(__name__)

class FiltreReply(Filtre):

  solicitant=None
  ticket_id=None

  def es_aplicable(self):
    logger.info("Filtre de reply");

    try:
      # Ara anem a veure que podem fer amb aquest missatge
      subject = self.msg.get_subject_ascii()
      logger.info ("Buscant numero a  %s" % subject);
      p=re.compile(settings.regex_reply)
      m = p.match(subject)
      self.ticket_id=m.group(1)

      logger.info ("Trobat ticket %s" % self.ticket_id);

      # Mirem si es un ticket valid
      ticket=self.tickets.consulta_tiquet(codi=self.ticket_id)

      # Mirem qui ha creat el ticket
      self.solicitant=ticket['solicitant']
      persona=self.persones.obtenir_dades_persona(self.solicitant)

      logger.info ("Ticket de %s" % self.solicitant);

      # Mirem si la persona que ha enviat el mail es la mateixa que ha creat el ticket
      # return self.msg.enviat_per(persona)

      # Proves! No mirem que sigui del mail origen per provar una mica mes de flexibilitat (per si contesta des de casa) 

      self.solicitant=self.persones.obtenir_uid(self.msg.get_from())
      logger.info ("Mail de %s" % self.solicitant);
      return self.solicitant!=None

    except:
      logger.info ("Peta el filtre...");
      return False

  def filtrar(self):
    body=self.msg.get_body()
    resultat=self.tickets.afegir_comentari_tiquet(
      codiTiquet=self.ticket_id,
      usuari=self.solicitant, 
      descripcio=("[Comentari afegit automaticament des de mail a %s ]<br><br>" % time.strftime("%c")) +body,
      tipusComentari='COMENT_TIQUET_PUBLIC',
      esNotificat='S')

    if resultat['codiRetorn']!="1":
      logger.info(resultat['descripcioError'])
      return False

    self.afegir_attachments(self.ticket_id,self.solicitant)

    logger.info("Comentari afegit")
    return True

