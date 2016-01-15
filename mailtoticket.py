#!/usr/bin/python
from mailticket import MailTicket
import settings
import filtres
import correu

import sys
import getopt
import logging
from StringIO import StringIO

logger = logging.getLogger()

if __name__ == '__main__':
  a=None
  opts, args = getopt.getopt(sys.argv[1:], 'c:')
  for o, a in opts:
    if o=='-c': settings.load(a)

  logging.basicConfig(
    filename=settings.get("log_file"),
    level=settings.get("log_level"),
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )

  buffer_logs = StringIO()
  logger.addHandler(logging.StreamHandler(buffer_logs))

  if a is not None:
    logger.info("Fitxer de configuracio [%s]",a)

  estat="UNKNOWN"
  tractat=False
  try:
    logger.info("-----------------------------------------------------")
    logger.info("Llegeixo mail")
    mail = MailTicket(sys.stdin)
    logger.info("Mail de %s llegit" % mail.get_from())
    if mail.cal_tractar():
      if filtres.aplicar_filtres(mail):
        tractat=True
        estat="SUCCESS"
        logger.info("Marco el mail com a tractat")
    else:
      estat="SKIP"
      logger.info("No cal tractar el mail %s" % mail.get_subject_ascii())
  except Exception, e:
    estat="ERROR"
    logger.exception("Ha petat algun dels filtres i no marco el mail com a tractat")
  finally:
    print "X-Mailtoticket: %s" % estat
    print mail
    logger.info("-----------------------------------------------------")
    if not tractat and settings.get("notificar_errors"):
      correu.enviar(buffer_logs.getvalue())
