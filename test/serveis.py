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
	

if __name__ == '__main__':
  unittest.main()
