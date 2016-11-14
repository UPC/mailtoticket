from filtres.nou import FiltreNou
import unittest
import mock
import testhelper
import settings
from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat


class TestTicketNou(unittest.TestCase):

    def setUp(self):
        self.mock_tickets = self.crear_mock_tickets()
        self.mock_identitat = self.crear_mock_identitat()
        settings.init()

    def crear_mock_tickets(self):
        tickets = mock.create_autospec(GestioTiquets)
        tickets.consulta_tiquet.return_value = {
            "solicitant": "usuari.qualsevol"}
        tickets.afegir_comentari_tiquet.return_value = {"codiRetorn": "1"}
        tickets.alta_tiquet.return_value = {
            "codiRetorn": "1", "codiTiquet": "666"}
        return tickets

    def crear_mock_identitat(self):
        identitat = mock.create_autospec(GestioIdentitat)
        identitat.obtenir_uid.return_value = "usuari.qualsevol"
        return identitat

    def test_filtra_signatura(self):
        """ Un mail amb signatura coneguda
        no ha de fer un attachment amb la signatura """
        settings.set("filtrar_attachments_per_hash", [
            "593e2391d469398a04b4d315e5793341"
        ])
        msg = testhelper.llegir_mail("attachment_signatura.txt")
        f = FiltreNou(msg, self.mock_tickets, self.mock_identitat)
        if f.es_aplicable():
            f.filtrar()
        self.assertEquals(
            self.mock_tickets.annexar_fitxer_tiquet.call_count, 0)

    def test_redirigit_per_usuari_concret(self):
        """ Un missatge reenviat per usuari.concret@example.com
        ha de crear-se a l'equip 11112 """
        settings.set("valors_defecte", [{
            "order": ['Resent-From'],
            "match": "^usuari.concret@example\.com$",
            "defaults": {"equipResolutor": "11112"}
        }])
        msg = testhelper.llegir_mail("mail_redirigit_usuari_concret.txt")
        self.assertEquals(msg.get_resent_from(), "usuari.concret@example.com")
        f = FiltreNou(msg, self.mock_tickets, self.mock_identitat)
        if f.es_aplicable():
            f.filtrar()
        self.assertEquals(
            self.mock_tickets.alta_tiquet.call_args_list[
                0][1]['equipResolutor'],
            '11112')

    def test_message_from_usuari_concret(self):
        """ Un missatge que ve de usuari.concret@example.com
        ha de crear-se a l'equip 11113 """
        settings.set("valors_defecte", [{
            "order": ['From'],
            "match": "^usuari.concret@example\.com$",
            "defaults": {"equipResolutor": "11113"}
        }])
        msg = testhelper.llegir_mail("mail_enviat_usuari_concret.txt")
        self.assertEquals(msg.get_from(), "usuari.concret@example.com")
        f = FiltreNou(msg, self.mock_tickets, self.mock_identitat)
        if f.es_aplicable():
            f.filtrar()
        self.assertEquals(
            self.mock_tickets.alta_tiquet.call_args_list[
                0][1]['equipResolutor'],
            '11113')

    def test_message_urgent(self):
        """ Un missatge amb la paraula URGENT al subject
        ha de crear-se amb gravetat alta """
        settings.set("valors_defecte", [{
            "order": ['Subject'],
            "match": ".*URGENT",
            "defaults": {"urgencia": "GRAVETAT_ALTA"}
        }])
        msg = testhelper.llegir_mail("urgent.txt")
        f = FiltreNou(msg, self.mock_tickets, self.mock_identitat)
        if f.es_aplicable():
            f.filtrar()
        self.assertEquals(
            self.mock_tickets.alta_tiquet.call_args_list[0][1]['urgencia'],
            'GRAVETAT_ALTA')

if __name__ == '__main__':
    unittest.main()
