import re
from soa.tiquets import *
from soa.identitat import *
from filtres.filtre import *


class FiltreReply(Filtre):

  solicitant=None
  ticket_id=None

  def es_aplicable(self):
    if self.msg.te_attachments():
      print "Multipart. Passem de tot!"
      return False

    # Ara anem a veure que podem fer amb aquest missatge
    subject = self.msg.get_subject()
    m = re.search('(\d+)', subject)
    self.ticket_id=m.group(0)

    # Mirem si es un ticket valid
    ticket=self.tickets.consulta_tiquet(codi=self.ticket_id)
    print "Gestionem reply a ticket ",self.ticket_id

    # Mirem qui ha creat el ticket
    self.solicitant=ticket['solicitant']
    persona=self.persones.obtenir_dades_persona(self.solicitant)
    print "Mail del creador ",persona['emailPreferent']

    self.solicitant=ticket['solicitant']

    # Mirem si la persona que ha enviat el ticket es la mateixa
    return self.msg.enviat_per(persona)

  def filtrar():
    body=msg.get_body()
    tickets.afegir_comentari_tiquet(
      codiTiquet=self.ticket_id,
      usuari=self.solicitant, 
      descripcio=body,
      tipusComentari='COMENT_TIQUET_PUBLIC',
      esNotificat='N')
    print "Comentari afegit al ticket"
    # TODO: aqui toca el tema dels adjunts

