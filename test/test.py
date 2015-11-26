from filtres.filtre import Filtre
from filtres.reply import FiltreReply
from filtres.nou import FiltreNou
import filtres
import testbase

class TestMailTicket(testbase.TestBase):

  def test_message_to_webmaster(self):
    """ Un missatge redirigit a webmaster-proves ha de tenir el "to" a webmaster-proves """
    msg=self.llegir_mail("redirected.txt")
    self.assertEquals(msg.get_to(),"webmaster-proves@fib.upc.edu")

  def test_message_marycruz(self):
    """ Un de la maricruz redirigit a webmaster-proves ha de mantenir les dos adreces """
    msg=self.llegir_mail("marycruz.txt")
    self.assertEquals(msg.get_from(),"marycruz@fib.upc.edu")
    self.assertEquals(msg.get_to(),"webmaster-proves@fib.upc.edu")

  def test_message_oromero(self):
    msg=self.llegir_mail("oromero.txt")
    self.assertEquals(msg.get_from(),"oromero@essi.upc.edu")

  def test_mailticket_reserva(self):
    msg=self.llegir_mail("reserva.txt")
    self.assertEquals(msg.get_to(),"lcfib-proves@fib.upc.edu")

  def test_mailticket_no_attach(self):
    msg=self.llegir_mail("reply3.txt")
    self.assertTrue(not msg.te_attachments())

  def test_mailticket_attach(self):
    """ Un mail amb attachmens ha de retornar que te attachments """
    msg=self.llegir_mail("reply2.txt")
    self.assertTrue(msg.te_attachments())

  def test_mailticket_no_attach(self):
    """ Un mail sense attachments ha de retornar que no te attachments """
    msg=self.llegir_mail("reply4.txt")
    self.assertTrue(not msg.te_attachments())

  def test_mailticket_petar(self):
    """ El mail de petar sembla que tingui diferents encodings al mateix temps """
    msg=self.llegir_mail("petar.txt")
    self.assertTrue(msg.get_body())
	
  def test_mailticket_base64(self):
    """ Mail condificat en base64 """
    msg=self.llegir_mail("manel-base64.txt")
    self.assertTrue(msg.get_body())
    self.assertTrue(msg.cal_tractar())
	
  def test_mailticket_jdelgado(self):
    """ Mail de justificant de recepcio que no s'ha de tractar """
    msg=self.llegir_mail("jdelgado.txt")
    self.assertFalse(msg.cal_tractar())

  def test_mailticket_jdelgado(self):
    """ Mail de justificant de recepcio de Notes que no s'ha de tractar """
    msg=self.llegir_mail("receipt.txt")
    self.assertFalse(msg.cal_tractar())
	
  def test_mailticket_jdelgado(self):
    """ Delivery failure """
    msg=self.llegir_mail("calabuig.txt")
    self.assertFalse(msg.cal_tractar())	

  def test_mailticket_reply_to(self):
    """ Obtenim la persona a partir del reply-to """
    msg=self.llegir_mail("andujar.txt")
    self.assertEquals(msg.get_reply_to(),"andujar@lsi.upc.edu")

  def test_mailticket_charset_raro(self):
    """ Possible error de conversio de charset """
    msg=self.llegir_mail("martin.txt")
    self.assertEquals(msg.get_from(),"martin@essi.upc.edu")

class TestFiltreReply(testbase.TestBase):

  def test_reply_sense_attachment(self):
    """ Donar un mail de reply sense attachments d'un usuari que troba ha de ser aplicable """ 
    msg=self.llegir_mail("reply.txt")
    f=FiltreReply(msg,self.tickets,self.identitat)
    self.assertTrue(f.es_aplicable())

  def test_mailticket_mail_desconegut(self):
    """ Un reply a un ticket amb solicitant conegut d'un mail desconegut ha de quedar en nom del solicitant """
    msg=self.llegir_mail("reply6.txt")
    f=FiltreReply(msg,self.tickets,self.identitat)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(self.tickets.afegir_comentari_tiquet.call_args_list[0][1]['usuari']=='jaume.moral')
 
  def test_filtra_signatura(self):
    """ Un mail amb signatura coneguda no ha de fer un attachment amb la signatura """
    msg=self.llegir_mail("marycruz.txt")
    f=FiltreNou(msg,self.tickets,self.identitat)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertTrue(self.tickets.annexar_fitxer_tiquet.call_count==0)
	
  def test_aplicar_nou_desconegut(self):
    """ Un mail sense multipart/alternative ha de donar el html o el text a saco """ 
    self.identitat.obtenir_uid.return_value=None
    msg=self.llegir_mail("sabate.txt")
    self.assertTrue(msg.get_body())		

  def test_reply_numeros(self):
    """ Mail que no detecta correctament si es de reply """ 
    msg=self.llegir_mail("jdelgado2.txt")
    f=FiltreReply(msg,self.tickets,self.identitat)
    if f.es_aplicable():
      f.filtrar()
    self.assertEquals(self.tickets.afegir_comentari_tiquet.call_args_list[0][1]['codiTiquet'],'581611')

  def test_reply_privat(self):
    """ Si fem un reply d'un comentari privat, el comentari ha de ser privat """ 
    msg=self.llegir_mail("privat.txt")
    f=FiltreReply(msg,self.tickets,self.identitat)
    if f.es_aplicable():
      f.filtrar()
    self.assertEquals(self.tickets.afegir_comentari_tiquet.call_args_list[0][1]['tipusComentari'],'COMENT_TIQUET_PRIVAT')

  def test_message_resent_from_jaumem(self):
    """ Un missatge reenviat per jaumem a de crear-se a l'equip 11112 encara que vagi a inlab """
    msg=self.llegir_mail("sabate.txt")
    self.assertEquals(msg.get_resent_from(),"jaumem@fib.upc.edu")
    f=FiltreNou(msg,self.tickets,self.identitat)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertEquals(self.tickets.alta_tiquet.call_args_list[0][1]['equipResolutor'],'11112')

  def test_message_from_jaume(self):
    """ Un missatge que ve de jaumem a de crear-se a l'equip 11112 encara que vagi a inlab """
    msg=self.llegir_mail("jaume.txt")
    self.assertEquals(msg.get_from(),"jaume.moral@upc.edu")
    f=FiltreNou(msg,self.tickets,self.identitat)
    if f.es_aplicable(): 
       f.filtrar()
    self.assertEquals(self.tickets.alta_tiquet.call_args_list[0][1]['equipResolutor'],'11113')



class TestAplicarFiltres(testbase.TestBase):

  def test_aplicar_reply(self):
    """ Donat un mail de reply sense attachments d'un usuari que troba ha de retornar true i crear comentari """ 
    msg=self.llegir_mail("reply.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.identitat)
    self.assertTrue(resultat)
    self.assertTrue(self.tickets.afegir_comentari_tiquet.called)
    self.assertFalse(self.tickets.alta_tiquet.called)

  def test_aplicar_nou(self):
    """ Donat un mail nou ha de dir que aplica i que crea ticket """ 
    msg=self.llegir_mail("nou.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.identitat)
    self.assertTrue(resultat)
    self.assertTrue(self.tickets.alta_tiquet.called)
    self.assertFalse(self.tickets.afegir_comentari_tiquet.called)

  def test_aplicar_nou_desconegut(self):
    """ Donat un mail desconegut ha de retornar false """ 
    self.identitat.obtenir_uid.return_value=None
    msg=self.llegir_mail("nou.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.identitat)
    self.assertFalse(resultat)	
	
  def test_aplicar_nou_mail_diferent(self):
    """ Donat un mail diferent de l'oficial, el ticket s'ha de crear per la persona pero al mail que ha donat """ 
    msg=self.llegir_mail("jaume.txt")
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.identitat)    
    self.assertTrue(self.tickets.alta_tiquet.called)
    self.assertEquals(self.tickets.modificar_tiquet.call_args_list[0][1]['emailSolicitant'],'jaume.moral@upc.edu')	

  def test_aplicar_nou_sense_subject(self):
    """ Un mail sense subject ha de crear ticket amb subject "Ticket sense subject" """ 
    msg=self.llegir_mail("sense.txt")
    self.assertEquals(msg.get_subject(),'')
    resultat=filtres.aplicar_filtres(msg,self.tickets,self.identitat)
    self.assertTrue(resultat)  	
    self.assertTrue(self.tickets.alta_tiquet.called)
    self.assertEquals(self.tickets.alta_tiquet.call_args_list[0][1]['assumpte'],'Ticket sense subject')


if __name__ == '__main__':
  unittest.main()
