import re

class Filtre:

  def __init__(self,msg,tickets,persones):
    self.msg=msg
    self.tickets=tickets
    self.persones=persones

  def es_aplicable(self):
    return False

  def filtrar(self):
    return

  def comprovar_attachment_valid(self,ctype,fitxer):
    # Si no tenim filename, es una imatge incrustada
    if fitxer==None:
      if ctype in ['image/jpeg','image/png','image/gif']:
        return True 
      else:
        return False
    # I si tenim filename, que no sigui un dels que filtrem
    for f in settings.filtrar_attachments:
      p=re.compile(f)
      if p.match(fitxer):
        return False
    return True

  def afegir_attachments(self,ticket_id,username):
    logger.info("Tractem attachments del ticket %s" % ticket_id)
    i=0;
    for a in self.msg.get_attachments():
      ctype=a.get_content_type()
      fitxer=a.get_filename()
      i+=1
      logger.info("Provem attachment %d %s" % (i,ctype))
      if self.comprovar_attachment_valid(ctype,fitxer):
        if fitxer==None:
          fitxer='attach%d.%s' % (i,ctype.split("/")[1])
        logger.info("Afegim attachment: %s" % fitxer)
        self.tickets.annexar_fitxer_tiquet(ticket_id,username,fitxer,a.get_payload())
      else:
        logger.info("Descartem attachment: %s" % a.get_filename())
