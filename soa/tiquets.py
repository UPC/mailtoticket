#!/usr/bin/python

from suds.client import Client
from SOAService import *
from settings import *

class GestioTiquets(SOAService):

  username_gn6=settings.username_gn6
  password_gn6=settings.password_gn6
  domini=settings.domini

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
