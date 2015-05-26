from settings import settings
from soa.service import SOAService

class GestioIdentitat(SOAService):

  username_soa=settings.get("username_soa_pre")
  password_soa=settings.get("password_soa_pre")

  url="https://bus-soades.upc.edu/GestioIdentitat/Personesv6?wsdl"

  mails_addicionals=settings["mails_addicionals"]

  def obtenir_uid(self,mail):  
    uid=None
    try:
      resultat=self.client.service.llistaPersones(email=mail)
      print resultat
      uid=resultat.llistaPersones.persona[0].cn
    except:
      try:
        uid=self.mails_addicionals[mail]
      except:
        uid=None
    finally:
      return uid
