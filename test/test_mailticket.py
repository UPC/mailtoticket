import unittest
import settings
import datetime
from mailticket import MailTicket


class TestMailTicket(unittest.TestCase):

    def setUp(self):
        settings.init()
        data = "From: foo@example.com\n" \
               "Date: Tue, 28 Sep 2016 10:24:09 +0200 (CEST)\n\n"
        self.mail = MailTicket(data)

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
        print d
        d.replace(tzinfo=None)
        print d
        self.assertEquals("28/09/2016 10:24", d.strftime("%d/%m/%Y %H:%M"))

    def test_get_date_invalid_format(self):
        # Un missatge amb la data en format "Apple Mail"
        data = "Date: 9/23/2016 11:04:10 AM\n\n"
        apple_mail = MailTicket(data)

        self.assertIsInstance(apple_mail.get_date(), datetime.datetime)

if __name__ == '__main__':
    unittest.main()
