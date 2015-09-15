from filtres.reply import FiltreReply
import settings

import logging
logger = logging.getLogger(__name__)

class FiltreReplyTancat(FiltreReplyTancat):

  def es_aplicable(self):
    logger.info("Filtre de Nou Extern, s'aplica sempre")
    self.solicitant=settings.get("usuari_extern")
    return True
