import unittest
from settings import settings,load_settings

class TestSettings(unittest.TestCase):

  def test_settings_normal(self):
    self.assertEquals(settings["domini"],1001)

  def test_settings_diferets(self):
#    load_settings("settings-diferents")
#    self.assertEquals(settings["domini"],999)


if __name__ == '__main__':
  unittest.main()
