from soa.identitat import GestioIdentitatLocal
import unittest
import settings
import testbase

class TestMails(testbase.TestBase):

  def test_patrons_mail(self):
    identitat=GestioIdentitatLocal()
    uid=identitat.obtenir_uid_local("jaume.moral@upc.edu")
    self.assertEquals("jaume.moral",uid)
    uid=identitat.obtenir_uid_local("usuari.qualsevol@upcnet.es")
    self.assertEquals("usuari.qualsevol",uid)
    uid=identitat.obtenir_uid_local("root@xxxx.ac.upc.edu")
    self.assertEquals("usuari.generic",uid)
    uid=identitat.obtenir_uid_local("root@ac.upc.edu")
    self.assertEquals("usuari.generic",uid)
    uid=identitat.obtenir_uid_local("root@xx.upc.edu")
    self.assertEquals(None,uid)

if __name__ == '__main__':
  unittest.main()
