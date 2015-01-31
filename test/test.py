from filtres.reply import FiltreReply
from filtres.nou import FiltreNou
from mailticket import MailTicket
from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
import filtres
import unittest
import mock
import logging
import tempfile
from settings import settings

def llegir_mail(msgfile): 
  fp = open("test/"+msgfile)
  mail_ticket=MailTicket(fp)
  fp.close()
  return mail_ticket

class TestBase(unittest.TestCase):
  def setUp(self):
    logging.basicConfig(filename=tempfile.gettempdir()+"/test.log",level=logging.DEBUG)
    self.tickets=mock.create_autospec(GestioTiquets)
    self.tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    self.tickets.afegir_comentari_tiquet.return_value={"codiRetorn":"1"}    
    self.tickets.alta_tiquet.return_value={"codiRetorn":"1","codiTiquet":"666"}    
    self.ldap=mock.create_autospec(GestioLDAP)
    self.ldap.obtenir_uid.return_value="jaume.moral"


class TestMailTicket(TestBase):

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


class TestFiltreReply(TestBase):

  def test_reply_sense_attachment(self):
    """ Donar un mail de reply sense attachments d'un usuari que troba ha de ser aplicable """ 
    msg=llegir_mail("reply.txt")
    f=FiltreReply(msg,self.tickets,self.ldap)
    self.assertTrue(f.es_aplicable())

  def test_mailticket_mail_desconegut(self):
    """ Un reply a un ticket amb solicitant conegut d'un mail desconegut ha de quedar en nom del solicitant """
    msg=llegir_mail("reply6.txt")
    f=FiltreReply(msg,self.tickets,self.ldap)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(self.tickets.afegir_comentari_tiquet.call_args_list[0][1]['usuari']=='jaume.moral')
 
  def test_filtra_signatura(self):
    """ Un mail amb signatura coneguda no ha de fer un attachment amb la signatura """
    msg=llegir_mail("marycruz.txt")
    f=FiltreNou(msg,self.tickets,self.ldap)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(self.tickets.annexar_fitxer_tiquet.call_count==0)

class TestAplicarFiltres(TestBase):

  def test_aplicar_reply(self):
    """ Donat un mail de reply sense attachments d'un usuari que troba ha de retornar true i crear comentari """ 
    msg=llegir_mail("reply.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.ldap)
    self.assertTrue(resultat)
    self.assertTrue(self.tickets.afegir_comentari_tiquet.called)
    self.assertFalse(self.tickets.alta_tiquet.called)

  def test_aplicar_nou(self):
    """ Donat un mail nou ha de dir que aplica i que crea ticket """ 
    msg=llegir_mail("nou.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.ldap)
    self.assertTrue(resultat)
    self.assertTrue(self.tickets.alta_tiquet.called)
    self.assertFalse(self.tickets.afegir_comentari_tiquet.called)

  def test_aplicar_nou_desconegut(self):
    """ Donat un mail desconegut ha de retornar false """ 
    self.ldap.obtenir_uid.return_value=None
    msg=llegir_mail("nou.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.ldap)
    self.assertFalse(resultat)


class TestServeis(TestBase):

  def desactivat_test_ldap(self):
    ldap=GestioLDAP()
    uid=ldap.obtenir_uid("juli@ac.upc.edu")
    self.assertEquals(uid,"julita.corbalan")


class TestSettings(unittest.TestCase):

  def test_settings_normal(self):
    self.assertEquals(settings["domini"],1001)


if __name__ == '__main__':
  unittest.main()
