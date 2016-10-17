from mailticket import MailTicket
import os


def llegir_mail(msgfile):
    fp = open(os.path.dirname(__file__) + "/mails/" + msgfile)
    mail_ticket = MailTicket(fp)
    fp.close()
    return mail_ticket
