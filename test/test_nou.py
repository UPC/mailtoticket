import unittest
import mock
import settings
import logging
import sys

from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat
from filtres.nou import FiltreNou
from mailticket import MailTicket


class TestNou(unittest.TestCase):

    def setUp(self):
        self.tickets = mock.create_autospec(GestioTiquets)
        self.tickets.alta_tiquet.return_value = {
            "codiRetorn": "1",
            "codiTiquet": "123"
        }
        self.tickets.modificar_tiquet.return_value = {
            "codiRetorn": "1",
        }
        self.tickets.afegir_solicitant_tiquet.return_value = {
            "codiRetorn": "1",
        }
        self.identitat = mock.create_autospec(GestioIdentitat)
        self.identitat.obtenir_uid.return_value = "usuari.real"

        self.msg = mock.create_autospec(MailTicket)
        self.msg.get_from.return_value = "mail.qualsevol@exemple.com"
        self.msg.get_cc.return_value = ["mail.qualsevol@exemple.com"]
        self.msg.get_subject.return_value = "Prova cc"

        settings.init()

    def test_mail_amb_cc_i_parametre_true_afegeix_solicitant(self):
        settings.set("afegir_solicitats_addicionals_en_cc", True)
        f = FiltreNou(self.msg, self.tickets, self.identitat)
        self.assertTrue(f.es_aplicable())
        f.filtrar()
        self.tickets.afegir_solicitant_tiquet.assert_called()

    def test_mail_amb_cc_i_parametre_false_no_afegeix_solicitant(self):
        settings.set("afegir_solicitats_addicionals_en_cc", False)
        f = FiltreNou(self.msg, self.tickets, self.identitat)
        self.assertTrue(f.es_aplicable())
        f.filtrar()
        self.tickets.afegir_solicitant_tiquet.assert_not_called()

    def test_mail_taguejat_amb_cc_afegeix_solicitant(self):
        self.msg.get_to.return_value = "mail.suport+cc@exemple.com"
        settings.set("afegir_solicitats_addicionals_en_cc", False)
        settings.set(
                     "afegir_solicitats_addicionals_en_cc_nomes_via",
                     r".*\+cc@.*")
        f = FiltreNou(self.msg, self.tickets, self.identitat)
        self.assertTrue(f.es_aplicable())
        f.filtrar()
        self.tickets.afegir_solicitant_tiquet.assert_called()


def showLogs():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)


if __name__ == '__main__':
    showLogs()
    unittest.main()
