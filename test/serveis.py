from soa.tiquets import GestioTiquets
from soa.identitat import GestioIdentitat
from settings import settings
import unittest
import time

class TestServeis(unittest.TestCase):

  def test_identitat(self):
    identitat=GestioIdentitat()
    uid=identitat.obtenir_uid("juli@ac.upc.edu")
    self.assertEquals(uid,"julita.corbalan")
	
  def test_estudiant(self):
    identitat=GestioIdentitat()
    uid=identitat.obtenir_uid("davidguerreromejias@gmail.com")
    self.assertEquals(uid,"david.guerrero")

  def test_pas(self):
    identitat=GestioIdentitat()
    uid=identitat.obtenir_uid("jaumem@fib.upc.edu")
    self.assertEquals(uid,"jaume.moral")    

  def test_pas_upc(self):
    identitat=GestioIdentitat()
    uid=identitat.obtenir_uid("desconegut@xx.edu")
    self.assertEquals(uid,None)

  def test_addicional(self):
    identitat=GestioIdentitat()
    uid=identitat.obtenir_uid("gestio.pfc@fib.upc.edu")
    self.assertEquals(uid,"laura.palanca")


if __name__ == '__main__':
  unittest.main()
