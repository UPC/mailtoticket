import settings
from soa.service import SOAService

class GestioIdentitat(SOAService):
  
  url="https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl"

  mails_addicionals=settings.get("mails_addicionals")

  def obtenir_uid(self,mail):  
    mail_canonic=mail.replace(".es",".edu")
    mail_canonic=mail_canonic.replace("@lsi","@cs")
    uid=None
    try:
      uid=self.mails_addicionals[mail_canonic]      
    except:
      try:
        resultat=self.client.service.llistaPersones(email=mail_canonic)
        uid=resultat.llistaPersones.persona[0].cn  
      except:
        uid=None
    finally:
      return uid
