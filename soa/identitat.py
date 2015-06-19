from settings import settings
from soa.service import SOAService

class GestioIdentitat(SOAService):
  
  url="https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl"

  mails_addicionals=settings["mails_addicionals"]

  def obtenir_uid(self,mail):  
    uid=None
    try:
      resultat=self.client.service.llistaPersones(email=mail)
      uid=resultat.llistaPersones.persona[0].cn
    except Exception as e:
      try:
        uid=self.mails_addicionals[mail]
      except:
        uid=None
    finally:
      return uid
