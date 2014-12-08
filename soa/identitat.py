#!/usr/bin/python

from suds.client import Client
from SOAService import *

class GestioIdentitat(SOAService):

  url="https://bus-soa.upc.edu/GestioIdentitat/Personesv5?wsdl"

  def obtenir_dades_persona(self,cn):
    return self.client.service.obtenirDadesPersona(commonName=cn)
