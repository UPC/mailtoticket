import unittest
import settings
from mock import patch, mock_open
from mailticket import MailTicket
import __builtin__


class TestMailTicket(unittest.TestCase):

    def setUp(self):
        settings.init()
        with patch.object(__builtin__, 'open',
                          mock_open(read_data="From: foo@example.com\n\n")):
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

if __name__ == '__main__':
    unittest.main()
