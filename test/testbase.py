from filtres.filtre import Filtre
from filtres.reply import FiltreReply
from filtres.nou import FiltreNou
from mailticket import MailTicket
from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat
from soa.identitat import GestioIdentitatLocal
import unittest
import mock
import logging
import tempfile
import settings

class TestBase(unittest.TestCase):
  def setUp(self):
    settings.load("settings_sample")
    logging.basicConfig(filename=tempfile.gettempdir()+"/test.log",level=logging.DEBUG)
    self.tickets=mock.create_autospec(GestioTiquets)
    self.tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    self.tickets.afegir_comentari_tiquet.return_value={"codiRetorn":"1"}    
    self.tickets.alta_tiquet.return_value={"codiRetorn":"1","codiTiquet":"666"}    
    self.identitat=mock.create_autospec(GestioIdentitat)
    self.identitat.obtenir_uid.return_value="jaume.moral"

  def test_base(self):
    self.assertTrue(True)

  def llegir_mail(self,msgfile): 
    fp = open("test/mails/"+msgfile)
    mail_ticket=MailTicket(fp)
    fp.close()
    return mail_ticket


if __name__ == '__main__':
  unittest.main()
