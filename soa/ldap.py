import subprocess
import settings

class GestioLDAP:

  def obtenir_uid(self,mail):
    try:
        p = subprocess.Popen(settings.busca_mail +" "+ mail, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result=None
        for line in p.stdout.readlines():
           result=line
        if result!=None:
           result=result.rstrip()
        else:
           result=settings.mails_addicionals[mail]
    except:
        result=None
    finally:
        return result
