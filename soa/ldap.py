import subprocess
from settings import settings
import re

class GestioLDAP:

  busca_mail=settings["busca_mail"]
  mails_addicionals=settings["mails_addicionals"]

  def obtenir_uid(self,mail):
  
    m = re.match("(.*)@upc.edu",mail)
    if m: 
        return m.group(1)
  
    try:
        p = subprocess.Popen(self.busca_mail +" "+ mail, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result=None
        for line in p.stdout.readlines():
           result=line
        if result!=None:
           result=result.rstrip()
        else:
           result=self.mails_addicionals[mail]
    except:
        result=None
    finally:
        return result
