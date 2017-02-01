# -*- coding: UTF-8 -*-

import netejahtml
import unittest
import settings
from testhelper import llegir_mail


class TestNeteja(unittest.TestCase):

    def setUp(self):
        settings.init()

    def test_neteja_reply6(self):
        msg = llegir_mail("reply6.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertTrue("vaig contestar?" in net)
        self.assertFalse("Usuari Qualsevol" in net)

    def test_neteja_mail_accents(self):
        msg = llegir_mail("mail-accents.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertTrue(u"què passa!" in net)
        self.assertFalse("amb prioritat" in net)

    def test_neteja_mail_office(self):
        msg = llegir_mail("mail-office.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertTrue("compte Atenea" in net)
        self.assertFalse("la matricula dels estudiants" in net)

    def test_neteja_reply_no_html(self):
        msg = llegir_mail("reply-no-html.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertTrue("Usuari" in net)
        self.assertFalse("contingut del vostre tiquet" in net)

    def test_neteja_pgp(self):
        msg = llegir_mail("pgp.txt")
        html = msg.get_body()
        net = netejahtml.treure_pgp(html)
        self.assertTrue("Us volia demanar" in net)
        self.assertTrue("Usuari" in net)
        self.assertTrue("mailtoticket" in net)
        self.assertFalse("PGP" in net)
        self.assertFalse("mQINB" in net)

    def test_treure_style(self):
        msg = llegir_mail("reply-mutipart-alternative.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertFalse("text-decoration" in net)

    def test_treure_script(self):
        msg = llegir_mail("reply-mutipart-alternative.txt")
        html = msg.get_body()
        net = netejahtml.neteja_reply(html)
        self.assertFalse("alert" in net)

if __name__ == '__main__':
    unittest.main()
