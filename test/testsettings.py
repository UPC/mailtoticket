import unittest
import settings as settings

class TestSettings(unittest.TestCase):

  def test_settings_normal(self):
    self.assertEquals(settings.settings["domini"],1001)

  def test_settings_diferets(self):
    # Com puc fer que aixo afecti a tot!!!!
    import settings_sample as settings
    self.assertEquals(settings.settings["domini"],999)

if __name__ == '__main__':
  unittest.main()
