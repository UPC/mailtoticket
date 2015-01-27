from suds.client import Client
from soa.service import SOAService

class GestioIdentitat(SOAService):

  url="https://bus-soa.upc.edu/GestioIdentitat/Personesv5?wsdl"

  def obtenir_dades_persona(self,cn):
    return self.client.service.obtenirDadesPersona(commonName=cn)
