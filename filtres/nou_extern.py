from filtres.nou import FiltreNou
import settings

import logging
logger = logging.getLogger(__name__)

class FiltreNouExtern(FiltreNou):

  def es_aplicable(self):
    logger.info("Filtre de Nou Extern, s'aplica sempre")
    self.solicitant=settings.get("usuari_extern")
    return True
