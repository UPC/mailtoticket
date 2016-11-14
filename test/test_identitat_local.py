from soa.identitat import GestioIdentitatLocal
import settings
import unittest


class TestIdentitatLocal(unittest.TestCase):

    def test_patrons_mail(self):
        settings.init()
        settings.set("patrons_mail_addicionals", {
            "^root@([a-z0-9.\-]+\.)?domain\.example\.com$": "usuari.generic",
            "^(.*)@example.edu$": "%s",
            "^(.*)@example.org$": "%s"
        })
        identitat = GestioIdentitatLocal()
        uid = identitat.obtenir_uid_local("usuari.qualsevol@example.edu")
        self.assertEquals("usuari.qualsevol", uid)
        uid = identitat.obtenir_uid_local("usuari.qualsevol@example.org")
        self.assertEquals("usuari.qualsevol", uid)
        uid = identitat.obtenir_uid_local("root@xxxx.domain.example.com")
        self.assertEquals("usuari.generic", uid)
        uid = identitat.obtenir_uid_local("root@domain.example.com")
        self.assertEquals("usuari.generic", uid)
        uid = identitat.obtenir_uid_local("root@xx.example.com")
        self.assertEquals(None, uid)

if __name__ == '__main__':
    unittest.main()
