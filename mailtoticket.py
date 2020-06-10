#!/usr/bin/python
# -*- coding: utf-8 -*-
from mailticket import MailTicket
import settings
import filtres
import correu
import optparse
import sys
import logging
from StringIO import StringIO

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()

ERROR = "ERROR"
SUCCESS = "SUCCESS"
SKIP = "SKIP"
REJECT = "REJECT"
UNKNOWN = "UNKNOWN"


def codi_sortida(estat):
    if estat == SUCCESS or estat == SKIP:
        return 0
    if estat == ERROR:
        return 1
    if estat == REJECT:
        return 2
    if estat == UNKNOWN:
        return 3

    # should not reach
    return -1


if __name__ == '__main__':
    a = None
    parser = optparse.OptionParser(description='Mailtoticket: Eina per \
    aconseguir que els mails enviats a una certa adreça es converteixin \
    automàticament en tickets, aprofitant els serveis web que ja ens \
    proporciona GN6 a tal efecte.')

    parser.add_option('-c',
                      action="store", dest="configfile",
                      help="Fitxer de configuració amb tots els paràmetres \
                      requerits.\n NOTA: Hi ha un exemple al fitxer \
                      settings_sample.py.", default="")

    options, args = parser.parse_args()

    # No file passed in params
    if options.configfile == '':
        print ("Falta fitxer de configuració com a paràmetre. \n Executar \
            mailtoticket.py -h per mostrar l'ajuda.")
        sys.exit(2)

    # Load file with default values
    settings.load(options.configfile.split('.')[0])

    logging.basicConfig(
        filename=settings.get("log_file"),
        level=settings.get("log_level"),
        format='%(asctime)s [%(process)d] %(name)-12s'
        ' %(levelname)-8s %(message)s'
    )

    buffer_logs = StringIO()
    logger.addHandler(logging.StreamHandler(buffer_logs))

    logger.info("Fitxer de configuració [%s]", options.configfile)

    estat = UNKNOWN
    tractat = False
    try:
        logger.info("-----------------------------------------------------")
        logger.info("Llegeixo mail")
        mail = MailTicket(sys.stdin)  # Reads from mail queue
        logger.info("Mail de %s llegit amb ID %s"
                    % (mail.get_from(), mail.get_header('message-id')))
        if mail.cal_tractar():
            if filtres.aplicar_filtres(mail):
                tractat = True
                estat = SUCCESS
                logger.info("Marco el mail com a tractat")
            else:
                estat = REJECT
                logger.info("Rebutjo el mail per no passar els filtres")

        else:
            estat = SKIP
            logger.info("No cal tractar el mail %s" % mail.get_subject_ascii())
    except Exception as e:
        estat = ERROR
        logger.exception(
            "Ha petat algun dels filtres i no marco el mail com a tractat"
        )
    finally:
        mail.msg['X-Mailtoticket'] = estat
        print mail
        logger.info("-----------------------------------------------------")
        if not tractat and settings.get("notificar_errors"):
            correu.enviar(buffer_logs.getvalue(), mail.msg)

        sys.exit(codi_sortida(estat))
