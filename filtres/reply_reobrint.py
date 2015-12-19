from filtres.reply import FiltreReply

import logging
logger = logging.getLogger(__name__)

class FiltreReplyReobrint(FiltreReply):

  def es_aplicable(self):
    if not FiltreReply.es_aplicable(self):
      return False

    # Si esta tancat, mirem de reobrir i si no podem, retornem False

    if self.ticket['estat']=='TIQUET_STATUS_TANCAT':
      logger.info ("Reobrim el ticket tancat %s" % self.ticket_id)
      self.tickets.modificar_tiquet(
        codiTiquet=self.ticket_id,
        estat='TIQUET_STATUS_OBERT'
      )
      self.ticket=self.tickets.consulta_tiquet(codi=self.ticket_id)
      if self.ticket['estat']=='TIQUET_STATUS_TANCAT':
        logger.info ("No podem reobrir el ticket %s. El filtre no es aplicable" % self.ticket_id)
        return False

    # Si hem arribat fins aqui, es que es aplicable
    return True
