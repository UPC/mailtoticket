import unittest
import mock
import settings
from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat
from filtres.reply import FiltreReply
from mailticket import MailTicket


class TestReply(unittest.TestCase):

    def setUp(self):
        self.tickets = mock.create_autospec(GestioTiquets)
        self.tickets.consulta_tiquet_dades.return_value = {
            "solicitant": "usuari.real",
            "emailSolicitant": "mail.extern@mail.com"
        }
        self.identitat = mock.create_autospec(GestioIdentitat)
        self.identitat.obtenir_uid.return_value = None

        settings.init()
        settings.set("regex_reply", "(.*)")  # Una que trobi sempre algo
        settings.set("regex_privat", "X")   # Una que no trobi mai res
        settings.set("usuari_extern", "usuari.extern")

    def test_reply_mail_extern_igual_a_solicitant_detecta_usuari_real(
            self):
        msg = mock.create_autospec(MailTicket)
        msg.get_from.return_value = "mail.extern@mail.com"
        msg.get_subject.return_value = "Re: ticket de prova"
        f = FiltreReply(msg, self.tickets, self.identitat)

        self.assertTrue(f.es_aplicable())
        self.assertEquals(f.solicitant, 'usuari.real')

    def test_reply_mail_extern_diferent_a_solicitant_detecta_usuari_extern(
            self):
        msg = mock.create_autospec(MailTicket)
        msg.get_from.return_value = "mail.extern.diferent@mail.com"
        msg.get_subject.return_value = "Re: ticket de prova"
        f = FiltreReply(msg, self.tickets, self.identitat)

        self.assertTrue(f.es_aplicable())
        self.assertEquals(f.solicitant, 'usuari.extern')

    def test_reply_ticket_id_dintre_de_message_id(
            self):
        msg = mock.create_autospec(MailTicket)
        msg.get_header.return_value = "<4b3b6b9c-bd31-tiquet-id-657421@gn6>"
        msg.get_subject.return_value = "Re: ticket de prova"
        f = FiltreReply(msg, self.tickets, self.identitat)

        self.assertTrue(f.es_aplicable())
        self.assertEquals(f.ticket_id, "657421")


if __name__ == '__main__':
    unittest.main()
