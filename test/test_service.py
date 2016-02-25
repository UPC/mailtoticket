import unittest

from soa.identitat import GestioIdentitatLocal


class TestService(unittest.TestCase):
    
    service = GestioIdentitatLocal()

    def test_resultat_erroni_true(self):
        resultat = {'codiRetorn': "2"}
        self.assertTrue(self.service.resultat_erroni(resultat))
        
    def test_resultat_erroni_false(self):
        resultat = {'codiRetorn': "1"}
        self.assertFalse(self.service.resultat_erroni(resultat))
        
    def test_retorna_missatge_error(self):
        resultat = {'codiRetorn': "2", 'descripcioError': 'peta'}
        self.assertEquals("Error: 2 - peta", self.service.retorna_missatge_error(resultat))
        
if __name__ == '__main__':
    unittest.main()
