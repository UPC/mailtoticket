import settings
import re
from soa.service import SOAService


class GestioIdentitat(SOAService):

    def __init__(self):
        self.url = "https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl"
        self.identitat_local = GestioIdentitatLocal()
        SOAService.__init__(self)

    def canonicalitzar_mail(self, mail):
        if mail is None:
            return None
        mail_canonic = mail.lower()
        mail_canonic = mail_canonic.replace(".upc.es", ".upc.edu")
        mail_canonic = mail_canonic.replace("@lsi", "@cs")
        return mail_canonic

    def obtenir_uid(self, mail):
        mail_canonic = self.canonicalitzar_mail(mail)
        uid = self.identitat_local.obtenir_uid_de_llista(mail_canonic)
        if uid is None:
            uid = self.obtenir_uid_remot(mail_canonic)

        if uid is None:
            uid = self.identitat_local.obtenir_uid_de_patrons(mail_canonic)

        return uid

    def obtenir_uid_remot(self, mail):
        uid = None
        try:
            resultat = self.client.service.llistaPersones(email=mail)
            if len(resultat.llistaPersones.persona) == 1:
                # Quan tenim un resultat, es aquest
                uid = resultat.llistaPersones.persona[0].cn
            else:
                # Si tenim mes d'un, busquem el que te el mail que busquem
                # com a preferent o be retornem el primer
                for persona in resultat.llistaPersones.persona:
                    dades_persona = self.client.service.obtenirDadesPersona(
                        commonName=persona.cn)
                    emailPreferent = getattr(
                        dades_persona,
                        'emailPreferent',
                        None)
                    if (self.canonicalitzar_mail(emailPreferent) == mail):
                        uid = persona.cn
                        return uid

                if uid is None:
                    uid = resultat.llistaPersones.persona[0].cn
        except:
            uid = None
        finally:
            return uid


class GestioIdentitatLocal:

    def __init__(self):
        self.mails_addicionals = settings.get("mails_addicionals")
        self.patrons_mails_addicionals \
            = settings.get("patrons_mail_addicionals")

    def obtenir_uid_local(self, mail):
        uid = self.obtenir_uid_de_llista(mail)
        if uid is None:
            uid = self.obtenir_uid_de_patrons(mail)

        return uid

    def obtenir_uid_de_llista(self, mail):
        try:
            return self.mails_addicionals[mail]
        except:
            return None

    def obtenir_uid_de_patrons(self, mail):
        try:
            for k, v in self.patrons_mails_addicionals.iteritems():
                patro = re.compile(k)
                m = patro.match(mail)
                if m:
                    try:
                        return v % m.group(1)
                    except:
                        return v

            return None
        except:
            return None
