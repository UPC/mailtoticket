import unittest
import settings
import datetime
from mailticket import MailTicket
from test.testhelper import llegir_mail
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
        self.mail.mails_no_ticket = [r'^.*@domain\.tld$']
        self.assertTrue(self.mail.cal_tractar())

    def test_mails_no_ticket_0004(self):
        self.mail.mails_no_ticket = [r'^.*@example\.com$']
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

    def test_encoding_xungo(self):
        mail = llegir_mail("encoding-xungo.txt")
        body = mail.get_body()
        self.assertNotEquals("", body)


if __name__ == '__main__':
    unittest.main()
