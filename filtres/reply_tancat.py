from filtres.reply import FiltreReply

import logging
logger = logging.getLogger(__name__)

class FiltreReplyTancat(FiltreReply):

  def filtrar(self):
    if self.ticket['estat']=='TIQUET_STATUS_TANCAT':
      logger.info ("Reobrim el ticket tancat %s" % self.ticket_id);
      self.tickets.modificar_tiquet(
        codiTiquet=self.ticket_id,
        estat='TIQUET_STATUS_OBERT'
      )
    super.filtrar(self)
