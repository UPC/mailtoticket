from filtres.reply import FiltreReply
from mailticket import MailTicket
from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
import unittest
import mock
import logging


def llegir_mail(msgfile): 
  print "-------------------"
  print "Llegint mail...",msgfile 
  fp = open("test/"+msgfile)
  mail_ticket=MailTicket(fp)
  fp.close()
  print "Llegit ",mail_ticket.get_subject()
  print "Attach ",len(mail_ticket.get_attachments())
  return mail_ticket


class TestFiltreReply(unittest.TestCase):

  def setUp(self):
    logging.basicConfig(filename="/tmp/test.log",level=logging.DEBUG)
    logger = logging.getLogger(__name__)

  def test_reply_sense_attachment(self):
    tickets=mock.create_autospec(GestioTiquets)
    tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    ldap=mock.create_autospec(GestioLDAP)
    ldap.obtenir_uid.return_value="jaume.moral"
    msg=llegir_mail("reply.txt")
    f=FiltreReply(msg,tickets,ldap)
    self.assertTrue(f.es_aplicable())

  def test_message_to_webmaster(self):
    msg=llegir_mail("redirected.txt")
    self.assertEquals(msg.get_to(),"webmaster-proves@fib.upc.edu")

  def test_message_marycruz(self):
    msg=llegir_mail("marycruz.txt")
    self.assertEquals(msg.get_from(),"marycruz@fib.upc.edu")
    self.assertEquals(msg.get_to(),"webmaster-proves@fib.upc.edu")

  def test_message_oromero(self):
    msg=llegir_mail("oromero.txt")
    self.assertEquals(msg.get_from(),"oromero@essi.upc.edu")

  def test_mailticket_reserva(self):
    msg=llegir_mail("reserva.txt")
    self.assertEquals(msg.get_to(),"lcfib-proves@fib.upc.edu")

  def test_mailticket_no_attach(self):
    msg=llegir_mail("reply3.txt")
    self.assertTrue(not msg.te_attachments());

  def test_mailticket_attach(self):
    msg=llegir_mail("reply2.txt")
    self.assertTrue(msg.te_attachments());

  def test_mailticket_no_attach(self):
    msg=llegir_mail("reply4.txt")
    self.assertTrue(not msg.te_attachments());

  def test_mailticket_mail_desconegut(self):
    tickets=mock.create_autospec(GestioTiquets)
    tickets.consulta_tiquet.return_value={"solicitant":"julita.corbalan"}
    tickets.afegir_comentari_tiquet.return_value={"codiRetorn":"1"}
    ldap=mock.create_autospec(GestioLDAP)
    ldap.obtenir_uid.return_value=None
    msg=llegir_mail("reply6.txt")
    f=FiltreReply(msg,tickets,ldap)
    if f.es_aplicable(): 
       print "eiiii"
       f.filtrar()
    print tickets.afegir_comentari_tiquet.call_args_list[0][1]['usuari']
    self.assertTrue(tickets.afegir_comentari_tiquet.call_args_list[0][1]['usuari']=='julita.corbalan')
 
  def test_ldap(self):
    ldap=GestioLDAP()
    uid=ldap.obtenir_uid("juli@ac.upc.edu")
    self.assertEquals(uid,"julita.corbalan")


if __name__ == '__main__':
  print "Testing..."
  unittest.main()

if __name__ == '__main__':
  print "Testing..."
  unittest.main()
