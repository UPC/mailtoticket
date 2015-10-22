import smtplib
import settings

def enviar(text):	
  de=settings.get("notificar_errors_from");
  a=settings.get("notificar_errors_to");
  host=settings.get("servidor_mail");
  subject="Informe d'errors de MailToTicket"
  server = smtplib.SMTP(host, 25)
  msg = "From: %s\nTo: %s\nSubject:%s\n\n%s" % (de,a,subject,text)
  server.sendmail(de, a, msg)
