import unittest
import settings

class TestSettings(unittest.TestCase):

  def test_settings_normal(self):
    settings.load()
    self.assertEquals(settings.get("domini"),999)

#  def test_settings_diferents(self):
#    settings.load("settings_diferents")
#    self.assertEquals(settings.get("domini"),1001)


if __name__ == '__main__':
  unittest.main()
