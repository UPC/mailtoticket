from settings import settings
from soa.service import SOAService

class GestioIdentitat(SOAService):

  username_soa=settings.get("username_soa_pre")
  password_soa=settings.get("password_soa_pre")

  url="https://bus-soades.upc.edu/GestioIdentitat/Personesv6?wsdl"

  def obtenir_uid(self,mail):  
    resultat=self.client.service.llistaPersones(email=mail)
    print resultat
    # TODO: falta veure l'estructura del resultat
    return "jaume.moral"