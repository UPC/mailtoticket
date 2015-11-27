import netejahtml
import unittest
from testbase import TestBase

class TestNeteja(TestBase):

  def test_neteja_reply6(self):
    msg=self.llegir_mail("reply6.txt")
    html=msg.get_body()
    net=netejahtml.neteja(html)
    self.assertTrue("vaig contestar?" in net)
    self.assertFalse("Julita Corbalan" in net)    

  def test_neteja_jaume(self):
    msg=self.llegir_mail("jaume-reply.txt")
    html=msg.get_body()
    net=netejahtml.neteja(html)
    self.assertTrue("utf8" in net)
    self.assertFalse("amb prioritat" in net)    

  def test_neteja_sabate(self):
    msg=self.llegir_mail("sabate.txt")
    html=msg.get_body()
    net=netejahtml.neteja(html)
    self.assertTrue("compte Atenea" in net)
    self.assertFalse("la matricula dels estudiants" in net)

  def test_neteja_martin(self):
    msg=self.llegir_mail("martin.txt")
    html=msg.get_body()
    net=netejahtml.neteja(html)
    self.assertTrue("Sandra" in net)
    self.assertFalse("contingut del vostre tiquet" in net)
    

if __name__ == '__main__':
  a=TestNeteja()
  #unittest.main()
