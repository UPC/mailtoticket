import unittest
import settings
import datetime
from mailticket import MailTicket
from testhelper import llegir_mail
from freezegun import freeze_time
from cStringIO import StringIO


class TestMailTicket(unittest.TestCase):

    def setUp(self):
        settings.init()
        data = "From: foo@example.com\n" \
               "Date: Tue, 28 Sep 2016 10:24:09 +0200 (CEST)\n\n"
        self.mail = MailTicket(StringIO(data))

    def test_mails_no_ticket_0001(self):
        self.mail.mails_no_ticket = ["foo@example.com"]
        self.assertFalse(self.mail.cal_tractar())

    def test_mails_no_ticket_0002(self):
        self.mail.mails_no_ticket = ["bar@example.com"]
        self.assertTrue(self.mail.cal_tractar())

    def test_mails_no_ticket_0003(self):
        self.mail.mails_no_ticket = ['^.*@domain\.tld$']
        self.assertTrue(self.mail.cal_tractar())

    def test_mails_no_ticket_0004(self):
        self.mail.mails_no_ticket = ['^.*@example\.com$']
        self.assertFalse(self.mail.cal_tractar())

    def test_get_date(self):
        d = self.mail.get_date()
        self.assertIsInstance(d, datetime.datetime)

    def test_get_body_buit(self):
        mail_buit = llegir_mail("mailbuit.txt")
        body = mail_buit.get_body()
        self.assertEquals("", body)

    def test_get_auto_submitted(self):
        mail_buit = llegir_mail("mailbuit.txt")
        mail_auto = llegir_mail("mailauto.txt")
        self.assertTrue(mail_auto.es_missatge_automatic())
        self.assertFalse(mail_buit.es_missatge_automatic())

    @freeze_time("2015-09-11 09:45", tz_offset=+2)
    def test_get_date_invalid_format(self):
        # Un missatge amb la data en format "Apple Mail"
        data = "Date: 9/23/2016 11:04:10 AM\n\n"
        apple_mail = MailTicket(StringIO(data))

        dt = apple_mail.get_date()
        self.assertEquals("11/09/2015 11:45", dt.strftime("%d/%m/%Y %H:%M"))

    def test_redirigit_passa_a_to(self):
        """ Un missatge redirigit a usuari.concret@example.com
        ha de tenir el "to" igual a usuari.concret@example.com """
        msg = MailTicket(StringIO(
            "Resent-To: usuari.concret@example.com\n"
            "To: altre.usuari@example.com"))
        self.assertEquals(msg.get_to(), "usuari.concret@example.com")

    def test_comprovar_from_to(self):
        """ Si un usuari.concret redirigeix a mailtoticket
        s'han de de mantenir les dos adreces """
        msg = MailTicket(StringIO(
            "From: usuari.concret@example.com\n"
            "Resent-To: mailtoticket@example.com"))
        self.assertEquals(msg.get_from(), "usuari.concret@example.com")
        self.assertEquals(msg.get_to(), "mailtoticket@example.com")

    def test_mailticket_multipart_alternative(self):
        msg = llegir_mail("reply-mutipart-alternative.txt")
        self.assertTrue(not msg.te_attachments())

    def test_mailticket_attach(self):
        """ Un mail amb attachmens ha de retornar que te attachments """
        msg = llegir_mail("reply-attachment.txt")
        self.assertTrue(msg.te_attachments())

if __name__ == '__main__':
    unittest.main()
