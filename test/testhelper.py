from mailticket import MailTicket
import os
from io import BytesIO


def llegir_mail(msgfile):
    fp = open(os.path.dirname(__file__) + "/mails/" + msgfile, "rb")
    mail_ticket = MailTicket(fp)
    fp.close()
    return mail_ticket


def string_to_mail(data):
    return BytesIO(data.encode())
