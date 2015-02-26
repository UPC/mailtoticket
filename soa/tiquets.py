from suds.client import Client
from soa.service import SOAService
from settings import settings

class GestioTiquets(SOAService):

  username_gn6=settings["username_gn6"]
  password_gn6=settings["password_gn6"]
  domini=settings["domini"]

  url = "https://bus-soa.upc.edu/gN6/GestioTiquetsv2?wsdl"

  def consulta_tiquet(self,codi):
    resultat=self.consulta_tiquets(codi=codi)
    return resultat.llistaTiquets[0]

  def consulta_tiquets(self,**kwargs):
    resultat=self.client.service.ConsultaTiquets(
      username=self.username_gn6,
      password=self.password_gn6,
      domini=self.domini,**kwargs)
    return resultat

  def afegir_comentari_tiquet(self,**kwargs):
    resultat=self.client.service.AfegirComentariTiquet(
      username=self.username_gn6,
      password=self.password_gn6,
      domini=self.domini,**kwargs)
    return resultat

  def alta_tiquet(self,solicitant,client='', assumpte='', descripcio='', equipResolutor='', assignatA='', producte='', subservei='', urgencia='GRAVETAT_MITJA', impacte='', proces='PROCES_AUS', procesOrigen='', estat='TIQUET_STATUS_OBERT', ip='', enviarMissatgeCreacio='S', enviarMissatgeTancament='N', imputacioAutomatica='N', infraestructura=''):
    resultat=self.client.service.AltaTiquet(
      self.username_gn6,
      self.password_gn6,
      self.domini,
      solicitant,
      client,
      assumpte,
      descripcio,
      equipResolutor,
      assignatA,
      producte,
      subservei,
      urgencia,
      impacte,
      proces,
      procesOrigen,
      estat,
      ip,
      enviarMissatgeCreacio,
      enviarMissatgeTancament,
      imputacioAutomatica,
      infraestructura)
    return resultat

  def annexar_fitxer_tiquet(self,codiTiquet,usuari,nomFitxer,fitxerBase64):
    resultat=self.client.service.AnnexarFitxerTiquet(
      self.username_gn6,
      self.password_gn6,
      self.domini,
      codiTiquet,
      usuari,
      nomFitxer,
      fitxerBase64)
    return resultat
	
  def modificar_tiquet(self,**kwargs):
    resultat=self.client.service.ModificarTiquet(
      username=self.username_gn6,
      password=self.password_gn6,
      domini=self.domini,**kwargs)
    return resultat
