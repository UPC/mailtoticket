#!/usr/bin/python

from filtres.reply import *
from filtres.nou import *
import email
from email.header import decode_header
from email.utils import parseaddr
import sys

class MailTicket:

  msg=None

  def __init__(self,msg):
    self.msg=msg

  def enviat_per(self,persona):
    email=parseaddr(self.msg['From'])[1]
    return email==persona['emailPreferent'].lower()

  def get_subject(self):
    subject=self.msg['Subject']
    resultat=""
    fragments=decode_header(subject)
    for fragment in fragments:
      resultat=resultat+fragment[0]+" "
    return resultat

  def get_body(self):
#    body=body.decode('utf-8')
    if not self.msg.is_multipart():
      return self.text2html(self.msg.get_payload())
    else:
      for part in self.msg.walk():
        if part.get_content_type() in ['text/plain']:
          return self.text2html(part.get_payload())
        if part.get_content_type() in ['text/html']:
          return part.get_payload()

  def text2html(self,text):
    return "<br>\n".join(text.split("\n"))

  def get_attachments(self):
    attachments=[]
    if self.msg.is_multipart():
      parts=self.msg.get_payload()
      trobat_body=False
      for part in self.msg.walk():        
        if not trobat_body:
          if part.get_content_type() in ['text/html','text/plain']: 
            trobat_body=True
        else:
          attachments.append(part.get_payload())
    return attachments

  def te_attachments(self):
    return len(self.get_attachments())>0


if __name__ == '__main__':
  mail = email.message_from_file(sys.stdin)
  msg=MailTicket(mail)

  tickets=GestioTiquets()
  persones=GestioIdentitat()

  filtres=[]
  filtres.append(FiltreReply(msg,tickets,persones))
  filtres.append(FiltreNou(msg,tickets,persones))

  print ".........................................."
  print msg.get_body()
  print ".........................................."
  print len(msg.get_attachments())
  print ".........................................."

  for filtre in filtres:
    print "Provo filtre "+filtre.__class__.__name__
    if filtre.es_aplicable():
      print "Es aplicable!"
      #filter.filtrar()
      exit