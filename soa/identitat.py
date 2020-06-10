# -*- coding: utf-8 -*-
import settings
import re
import requests
import ldap
import logging

logger = logging.getLogger()


class GestioIdentitat:

    def __init__(self):
        self.url = "https://identitatdigital.upc.edu/gcontrol/rest"
        self.token = self.get_token()
        self.identitat_local = GestioIdentitatLocal()

    def get_token(self):
        try:
            resposta = requests.post(self.url + "/acls/processos",
                                     data={'idProces': settings.get("identitat_digital_apikey")})
            token = resposta.json()['tokenAcl']
            return token
        except:
            return None

    def ldap_search(self, l, mail, base_search):
        # Scope has three options, SUBTREE searches all sub-folder/directories
        scope = ldap.SCOPE_SUBTREE
        # filter consists of a cn(common name) and keyword.
        # putting asterisks around our keyword will match anything containing the string
        # f = "cn=" + "*" + keyword + "*"
        # Searching by mail
        f = "(mail=" + mail + ')'
        # determines which attributes to return. Returns all if set to "None"
        retrieve_attributes = None
        result_set = []
        timeout = 0
        # Get all the fields for the ldap entry (COMMENT IN DEVELOPMENT MODE)
        result = l.search_s(base_search, scope, f, retrieve_attributes)
        # print result[0][1].keys()
        if len(result) != 0:
            dn = result[0][0]
            domain = dn.split(',' + base_search)[0].split('ou=')[-1]
        try:
            result_id = l.search(base_search, scope, f, retrieve_attributes)
            while 1:
                result_type, result_data = l.result(result_id, timeout)
                if(result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            if len(result_set) == 0:
                print "  No user found"
                return
            for i in range(len(result_set)):
                for entry in result_set[i]:
                    try:
                        cn = entry[1]['cn'][0]
                        logger.info("  cn: %s\n  dn: %s\n  domini: %s\n" % (cn, dn, domain))
                        return cn
                    except:
                        pass
        except ldap.LDAPError, e:
            print e

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

        if not uid:
            uid = self.obtenir_uid_remot(mail_canonic)

        if not uid:
            uid = self.identitat_local.obtenir_uid_de_patrons(mail_canonic)
        return uid

    def obtenir_uid_remot(self, mail):
        try:
            # Pot ser que un usuari d'un departament no tingui a identitat
            # digital un mail del tipus @upc.edu, aixi que primer comprovem
            # si la part esquerra del mail correspon a un usuari UPC real
            if "@upc.edu" in mail:
                try:
                    cn = mail.split("@")[0]
                    persona = requests.get(
                        self.url + "/externs/persones/" + cn + "/cn",
                        headers={'TOKEN': self.token}).json()
                    return persona['commonName']
                except:
                    None

            # Si no hi ha correspondencia directa amb un usuari UPC
            # busquem a partir del mail qui pot ser
            cns = requests.get(self.url + "/externs/identitats?email=" + mail,
                               headers={'TOKEN': self.token})

            # Si tenim resultats, són usuaris de GID (UPC/UPCNET)
            if cns.content != '':
                cns = cns.json()
                if 'errorResponse' in cns:
                    return "-- None -- (Error en la resposta del Gestor de la Identitat)."
                if len(cns) == 1:
                    # Quan tenim un resultat, es aquest
                    return cns['identitats'][0]['commonName']
                else:
                    # Si tenim mes d'un, busquem el que te el mail que busquem
                    # com a preferent o be retornem el primer
                    for cn in cns:
                        try:
                            persona = requests.get(
                                self.url + "/externs/persones/" + cn + "/cn",
                                headers={'TOKEN': self.token}).json()
                            email_preferent = persona['emailPreferent']
                            if (self.canonicalitzar_mail(email_preferent) == mail):
                                return persona['commonName']
                        except:
                            None
                    return None
            else:
                # Tractem els usuaris de fora de la UPC amb el LDAP externs
                # Initialize LDAP connection
                LDAP_SERVER_URL = settings.get("LDAP_SERVER_URL")
                LDAP_BIND_USER = settings.get("LDAP_BIND_USER")
                LDAP_PASSWORD = settings.get("LDAP_PASSWORD")
                LDAP_BASE_SEARCH = settings.get("LDAP_BASE_SEARCH")
                ldap_server = ldap.initialize(LDAP_SERVER_URL)
                try:
                    ldap_server.protocol_version = ldap.VERSION3
                    ldap_server.simple_bind_s(LDAP_BIND_USER, LDAP_PASSWORD)
                    logger.info("Connected to : " + LDAP_SERVER_URL)
                    logger.info("Search user  : " + mail)
                    username = self.ldap_search(ldap_server, mail, LDAP_BASE_SEARCH)
                    return username
                except Exception, error:
                    print error
        except Exception:
            return None


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
        except Exception:
            return None

    def obtenir_uid_de_patrons(self, mail):
        try:
            for k, v in self.patrons_mails_addicionals.iteritems():
                patro = re.compile(k)
                m = patro.match(mail)
                if m:
                    try:
                        return v % m.group(1)
                    except Exception:
                        return v

            return None
        except Exception:
            return None