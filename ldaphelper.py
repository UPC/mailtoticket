# -*- coding: utf-8 -*-
import settings
import ldap
import logging

logger = logging.getLogger()


class LDAP:
    """Classe d'ajuda per connectar amb ldap."""

    def __init__(self, mail):
        self.mail_to_find = mail

    def cerca_ldap(self, ldap_srv, mail, base_s):
        """Fa efectiva la cerca a ldap."""
        # Scope te tres opcions, SUBTREE cerca a totes les subcarpetes
        scope = ldap.SCOPE_SUBTREE
        # El filtre consisteix en un cn(common name) y una paraula clau.
        # Afegir asteriscs al voltant de la paraula clau permetrà retornar
        # qualsevol coincidencia.
        # f = "cn=" + "*" + keyword + "*"
        # P.e: cerca per mail
        f = "(mail=" + mail + ")"
        # Determina quins atributs han de retornar.
        # Retorna tot si es defineix a "None".
        retrieve_attributes = None
        result_set = []
        timeout = 0
        result = ldap_srv.search_s(base_s, scope, f, retrieve_attributes)
        if len(result) != 0:
            dn = result[0][0]
            domain = dn.split(',' + base_s)[0].split('ou=')[-1]
        try:
            result_id = ldap_srv.search(base_s, scope, f, retrieve_attributes)
            while 1:
                result_type, result_data = ldap_srv.result(result_id, timeout)
                if(result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            if len(result_set) == 0:
                logger.warning("No s'ha trobat cap usuari a ldap")
                return
            for i in range(len(result_set)):
                for entry in result_set[i]:
                    try:
                        cn = entry[1]['cn'][0] + '@' + domain
                        logger.info("cn: %s\n  dn: %s\n  domini: %s\n"
                                    % (cn, dn, domain))
                        return cn
                    except Exception:
                        pass
        except ldap.LDAPError as error:
            print(error)

    def obtenir_uid_ldap(self):
        """Configura la connexio amb ldap i prepara la cerca."""
        mail = self.mail_to_find
        LDAP_SERVER_URL = settings.get("LDAP_SERVER_URL")
        LDAP_BIND_USER = settings.get("LDAP_BIND_USER")
        LDAP_PASSWORD = settings.get("LDAP_PASSWORD")
        LDAP_BASE_SEARCH = settings.get("LDAP_BASE_SEARCH")
        ldap_srv = ldap.initialize(LDAP_SERVER_URL)
        try:
            ldap_srv.protocol_version = ldap.VERSION3
            ldap_srv.simple_bind_s(LDAP_BIND_USER, LDAP_PASSWORD)
            logger.info("Conectat a: " + LDAP_SERVER_URL)
            logger.info("Cercant usuari: " + mail)
            username = self.cerca_ldap(ldap_srv, mail,
                                       LDAP_BASE_SEARCH)

            logger.info("Correspon a un usuari extern")
            return username
        except Exception as error:
            logger.info("Error durant la cerca a LDAP")
            print(error)
