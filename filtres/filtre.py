class Filtre:

  def __init__(self,msg,tickets,persones):
    self.msg=msg
    self.tickets=tickets
    self.persones=persones

  def es_aplicable(self):
    return False

  def filtrar(self):
    return
