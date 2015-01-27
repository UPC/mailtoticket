from filtres.reply import *
from mailtoticket import *
from mock import *
import unittest


def llegir_mail(msgfile): 
  print "Llegint mail..."    
  fp = open(msgfile)
  msg = email.message_from_file(fp)
  fp.close()
  print "Llegit"    
  return MailTicket(msg)


class TestFiltreReply(unittest.TestCase):

  #TODO. El tema de mocking sembla que es de python 3.

  def setUp(self):
    self.tickets=Mock()
    self.tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    self.persones=Mock()
    self.persones.obtenir_dades_persona.return_value={"emailPreferent":"jaumem@fib.upc.edu"}

  def test_reply_sense_attachment(self):
    msg=llegir_mail("reply.txt")
    f=FiltreReply(msg,self.tickets,self.persones)
    self.assertTrue(f.es_aplicable())

  def test_reply_mail_attachment(self):
    msg=llegir_mail("reply2.txt")
    f=FiltreReply(msg,self.tickets,self.persones)
    self.assertFalse(f.es_aplicable())

if __name__ == '__main__':
  print "Testing..."
  unittest.main()
