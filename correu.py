from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
import smtplib
import settings
import logging
logger = logging.getLogger(__name__)


def enviar(text, orig):
    try:
        msgid = orig['Message-Id']
        de = settings.get("notificar_errors_from")
        a = settings.get("notificar_errors_to")
        host = settings.get("servidor_mail")
        subject = "Informe d'errors de MailToTicket"
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = de
        msg['To'] = a
        part1 = MIMEText(text, 'plain', 'utf8')
        part2 = MIMEMessage(orig, 'rfc822')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(host, 25)
        server.sendmail(de, a, msg.as_string())
        server.quit()
        logger.info("Informe d'errors de %s enviat per correu" % msgid)
    except Exception as e:
        logger.info(e)
        logger.info("No s'ha pogut enviar per correu l'informe d'errors de %s"
                    % msgid)
