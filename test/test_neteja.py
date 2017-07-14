# -*- coding: UTF-8 -*-

import netejahtml
import unittest
from testhelper import llegir_mail


class TestNeteja(unittest.TestCase):

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

    def test_treure_comentaris(self):
        msg = llegir_mail("comentaris.txt")
        html = msg.get_body()
        net = netejahtml.neteja_nou(html)
        print net
        self.assertFalse("supportList" in net)

if __name__ == '__main__':
    unittest.main()
