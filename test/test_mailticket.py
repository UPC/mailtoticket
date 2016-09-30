import unittest
import settings
import datetime
from mock import patch, mock_open
from mailticket import MailTicket
import __builtin__
from freezegun import freeze_time


class TestMailTicket(unittest.TestCase):

    def setUp(self):
        settings.init()
        data = "From: foo@example.com\n" \
               "Date: Tue, 28 Sep 2016 10:24:09 +0200 (CEST)\n\n"
        with patch.object(__builtin__, 'open', mock_open(read_data=data)):
            with open('foo') as fp:
                self.mail = MailTicket(fp)

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

    @freeze_time("2015-09-11 09:45", tz_offset=+2)
    def test_get_date_invalid_format(self):
        # Un missatge amb la data en format "Apple Mail"
        data = "Date: 9/23/2016 11:04:10 AM\n\n"
        with patch.object(__builtin__, 'open', mock_open(read_data=data)):
            with open('foo') as fp:
                apple_mail = MailTicket(fp)

        dt = apple_mail.get_date()
        self.assertEquals("11/09/2015 11:45", dt.strftime("%d/%m/%Y %H:%M"))

if __name__ == '__main__':
    unittest.main()
