import unittest
from soa.service import SOAService


class TestService(unittest.TestCase):

    def test_resultat_erroni_true(self):
        resultat = {'codiRetorn': "2"}
        self.assertTrue(SOAService.resultat_erroni(resultat))

    def test_resultat_erroni_false(self):
        resultat = {'codiRetorn': "1"}
        self.assertFalse(SOAService.resultat_erroni(resultat))


if __name__ == '__main__':
    unittest.main()
