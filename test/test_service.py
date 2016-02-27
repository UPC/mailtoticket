import unittest
from soa.service import SOAService


class TestService(unittest.TestCase):

    def test_resultat_erroni_true(self):
        resultat = {'codiRetorn': "2"}
        self.assertTrue(SOAService.resultat_erroni(resultat))

    def test_resultat_erroni_false(self):
        resultat = {'codiRetorn': "1"}
        self.assertFalse(SOAService.resultat_erroni(resultat))

    def test_retorna_missatge_error(self):
        resultat = {'codiRetorn': "2", 'descripcioError': 'peta'}
        self.assertEquals(
            "Error: 2 - peta", SOAService.retorna_missatge_error(resultat))

if __name__ == '__main__':
    unittest.main()
