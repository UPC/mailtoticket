import smtplib
import settings
import logging
logger = logging.getLogger(__name__)

def enviar(text):	
  try:
    de=settings.get("notificar_errors_from");
    a=settings.get("notificar_errors_to");
    host=settings.get("servidor_mail");
    subject="Informe d'errors de MailToTicket"
    server = smtplib.SMTP(host, 25)
    msg = "From: %s\nTo: %s\nSubject:%s\n\n%s" % (de,a,subject,text)
    server.sendmail(de, a, msg)
  except Exception, e:
  	logger.info(e)
  	logger.info("No s'ha pogut enviar l'informe d'error per correu")
