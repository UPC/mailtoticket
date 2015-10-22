import settings
import re
from soa.service import SOAService

class GestioIdentitat(SOAService):
  
  def __init__(self):
    self.url="https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl"
    self.mails_addicionals=settings.get("mails_addicionals")
    self.patrons_mails_addicionals=settings.get("patrons_mail_addicionals")
    SOAService.__init__(self)

  def canonicalitzar_mail(self,mail):
    mail_canonic=mail.lower()
    mail_canonic=mail_canonic.replace(".upc.es",".upc.edu")
    mail_canonic=mail_canonic.replace("@lsi","@cs")    
    return mail_canonic

  def obtenir_uid(self,mail):  
    mail_canonic=self.canonicalitzar_mail(mail)
    uid=self.obtenir_uid_local(mail_canonic)
    if uid!=None: return uid
    uid=self.obtenir_uid_remot(mail_canonic)
    return uid

  def obtenir_remot(self,mail):  
    uid=None
    try:
      resultat=self.client.service.llistaPersones(email=mail_canonic)
      if len(resultat.llistaPersones.persona)==1:
        # Quan tenim un resultat, es aquest
        uid=resultat.llistaPersones.persona[0].cn  
      else:
        # Si tenim mes d'un, busquem el que te el mail que busquem com a preferent o be retornem el primer
        for persona in resultat.llistaPersones.persona:
          dades_persona=self.client.service.obtenirDadesPersona(commonName=persona.cn)
          if (self.canonicalitzar_mail(dades_persona.emailPreferent)==mail_canonic):
            uid=persona.cn
        if uid==None:
          resultat.llistaPersones.persona[0].cn
    except:
      uid=None
    finally:
      return uid

  def obtenir_uid_local(self,mail):  
    mail_canonic=self.canonicalitzar_mail(mail)
    uid=None
    try:      
      uid=self.mails_addicionals[mail_canonic]      
    except:
      for k,v in self.patrons_mails_addicionals.iteritems():
        patro=re.compile(k)
        m=patro.match(mail)
        print k
        if m:
          print m.groups()
          if len(m.groups())>0:
            uid=v % m.group(1)
          else:
            uid=v
      return None
    finally:
      return uid
