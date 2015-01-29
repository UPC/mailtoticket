from filtres.reply import FiltreReply
from filtres.nou import FiltreNou
from mailticket import MailTicket
from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
import unittest
import mock
import logging


def llegir_mail(msgfile): 
  fp = open("test/"+msgfile)
  mail_ticket=MailTicket(fp)
  fp.close()
  return mail_ticket

class TestMailTicket(unittest.TestCase):

  def test_message_to_webmaster(self):
    """ Un missatge redirigit a webmaster-proves ha de tenir el "to" a webmaster-proves """
    msg=llegir_mail("redirected.txt")
    self.assertEquals(msg.get_to(),"webmaster-proves@fib.upc.edu")

  def test_message_marycruz(self):
    """ Un de la maricruz redirigit a webmaster-proves ha de mantenir les dos adreces """
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
    """ Un mail amb attachmens ha de retornar que te attachments """
    msg=llegir_mail("reply2.txt")
    self.assertTrue(msg.te_attachments());

  def test_mailticket_no_attach(self):
    """ Un mail sense attachments ha de retornar que no te attachments """
    msg=llegir_mail("reply4.txt")
    self.assertTrue(not msg.te_attachments());


class TestFiltreReply(unittest.TestCase):

  def test_reply_sense_attachment(self):
    """ Donar un mail de reply sense attachments d'un usuari que troba ha de ser aplicable """ 
    tickets=mock.create_autospec(GestioTiquets)
    tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    ldap=mock.create_autospec(GestioLDAP)
    ldap.obtenir_uid.return_value="jaume.moral"
    msg=llegir_mail("reply.txt")
    f=FiltreReply(msg,tickets,ldap)
    self.assertTrue(f.es_aplicable())

  def test_mailticket_mail_desconegut(self):
    """ Un reply a un ticket amb solicitant conegut d'un mail desconegut ha de quedar en nom del solicitant """
    tickets=mock.create_autospec(GestioTiquets)
    tickets.consulta_tiquet.return_value={"solicitant":"julita.corbalan"}
    tickets.afegir_comentari_tiquet.return_value={"codiRetorn":"1"}
    ldap=mock.create_autospec(GestioLDAP)
    ldap.obtenir_uid.return_value=None
    msg=llegir_mail("reply6.txt")
    f=FiltreReply(msg,tickets,ldap)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(tickets.afegir_comentari_tiquet.call_args_list[0][1]['usuari']=='julita.corbalan')
 
  def test_filtra_signatura(self):
    """ Un mail amb signatura coneguda no ha de fer un attachment amb la signatura """
    tickets=mock.create_autospec(GestioTiquets)
    tickets.consulta_tiquet.return_value={"solicitant":"marycruz.arancon"}
    tickets.alta_tiquet.return_value={"codiRetorn":"1","codiTiquet":"666"}
    ldap=mock.create_autospec(GestioLDAP)
    msg=llegir_mail("marycruz.txt")
    f=FiltreNou(msg,tickets,ldap)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(tickets.annexar_fitxer_tiquet.call_count==0)
 
class TestServeis(unittest.TestCase):

  def desactivat_test_ldap(self):
    ldap=GestioLDAP()
    uid=ldap.obtenir_uid("juli@ac.upc.edu")
    self.assertEquals(uid,"julita.corbalan")


if __name__ == '__main__':
  logging.basicConfig(filename="/tmp/test.log",level=logging.DEBUG)
  unittest.main()
