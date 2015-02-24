from soa.tiquets import GestioTiquets
from soa.ldap import GestioLDAP
from settings import settings
from test import TestBase

class TestServeis(TestBase):

  def test_ldap(self):
    ldap=GestioLDAP()
    uid=ldap.obtenir_uid("juli@ac.upc.edu")
    self.assertEquals(uid,"julita.corbalan")

  def test_comentari(self):
    tickets=GestioTiquets()
    resultat=tickets.afegir_comentari_tiquet(
      codiTiquet=549372 ,
      usuari="jaume.moral", 
      descripcio="[Comentari de prova creat en data %s ]" % time.strftime("%c"),
      tipusComentari='COMENT_TIQUET_PUBLIC',
      esNotificat='S')
    self.assertEquals(resultat['codiRetorn'],"1")

  def test_nou(self):
    tickets=GestioTiquets()
    resultat=tickets.alta_tiquet(
      assumpte="Prova ticket",
      solicitant="jaume.moral", 
      descripcio="[Tiquet creat automaticament des de testing a %s ]<br><br>" % time.strftime("%c"),
      equipResolutor=55633
      )
    self.assertEquals(resultat['codiRetorn'],"1")
	

if __name__ == '__main__':
  unittest.main()
