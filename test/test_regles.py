import unittest
import mock
import settings
from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat
from filtres.nou import FiltreNou
from mailticket import MailTicket
from test.testhelper import llegir_mail


class TestRegles(unittest.TestCase):

    def setUp(self):
        self.tickets = mock.create_autospec(GestioTiquets)
        self.identitat = mock.create_autospec(GestioIdentitat)
        settings.init()

    def test_regla_amb_cc_comprova_primer_valor(self):
        settings.set("valors_defecte",
                     [
                        {
                            "order": ["Cc"],
                            "match": "mail.qualsevol2@mail.com",
                            "defaults": {"equipResolutor": "666"}
                        }
                     ])
        msg = llegir_mail("cc.txt")
        f = FiltreNou(msg, self.tickets, self.identitat)
        defaults = f.obtenir_parametres_addicionals()
        self.assertEqual(defaults["equipResolutor"], "666")

    def test_regla_amb_cc_comprova_segon_valor(self):
        settings.set("valors_defecte",
                     [
                        {
                            "order": ["Cc"],
                            "match": "mail.qualsevol2@mail.com",
                            "defaults": {"equipResolutor": "666"}
                        }
                     ])
        msg = llegir_mail("cc.txt")
        f = FiltreNou(msg, self.tickets, self.identitat)
        defaults = f.obtenir_parametres_addicionals()
        self.assertEqual(defaults["equipResolutor"], "666")


if __name__ == '__main__':
    unittest.main()
