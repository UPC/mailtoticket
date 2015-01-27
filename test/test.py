from filtres.reply import *
from mailtoticket import *
from mock import *
import unittest


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
    self.tickets=Mock()
    self.tickets.consulta_tiquet.return_value={"solicitant":"jaume.moral"}
    self.persones=Mock()
    self.persones.obtenir_dades_persona.return_value={"emailPreferent":"jaumem@fib.upc.edu"}

  def test_reply_sense_attachment(self):
    msg=llegir_mail("reply.txt")
    f=FiltreReply(msg,self.tickets,self.persones)
    self.assertTrue(f.es_aplicable())

#  def test_reply_mail_attachment(self):
#    msg=llegir_mail("reply2.txt")
#    f=FiltreReply(msg,self.tickets,self.persones)
#    self.assertFalse(f.es_aplicable())

  def test_mailticket_no_attach(self):
    msg=llegir_mail("reply3.txt")
    self.assertTrue(not msg.te_attachments());

  def test_mailticket_attach(self):
    msg=llegir_mail("reply2.txt")
    self.assertTrue(msg.te_attachments());

  def test_mailticket_no_attach(self):
    msg=llegir_mail("reply4.txt")
    self.assertTrue(not msg.te_attachments());
 
#  def test_ldap(self):
#    print "ldap"
#    ldap=GestioLDAP()
#    uid=ldap.obtenir_uid("juli@ac.upc.edu")
#    self.assertEquals(uid,"julita.corbalan")


if __name__ == '__main__':
  print "Testing..."
  unittest.main()

if __name__ == '__main__':
  print "Testing..."
  unittest.main()
