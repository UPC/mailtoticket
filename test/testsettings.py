import settings
from testbase import TestBase

class TestSettings(TestBase):

  def test_settings_normal(self):
    self.assertEquals(settings.get("domini"),999)

#  def test_settings_diferents(self):
#    settings.load("settings_diferents")
#    self.assertEquals(settings.get("domini"),1001)


if __name__ == '__main__':
  unittest.main()
