import email
from email.header import decode_header
from email.utils import parseaddr


import logging
logger = logging.getLogger(__name__)

class MailTicket:
  """ Classe que encapsula un mail que es convertira en un ticket """

  msg=None
  part_body=0

  def __init__(self,file):
    self.msg = email.message_from_file(file)
    self.tracta_body()
    self.tracta_subject()

  def tracta_body(self):
    if not self.msg.is_multipart():
      part=self.msg
      body=self.codifica(part)
      self.body=self.text2html(body)
    else:
      self.part_body=0
      el_body_es_html=False
      for part in self.msg.walk():
        self.part_body=self.part_body+1
        if part.get_content_type() in ['multipart/alternative']:
          el_body_es_html=True
        if part.get_content_type() in ['text/html'] and el_body_es_html:
          self.body=self.codifica(part)
          break
        if part.get_content_type() in ['text/plain'] and not el_body_es_html:
          body=self.codifica(part)
          self.body=self.text2html(body)
          break

  def codifica(self,part):
    return unicode(part.get_payload(decode=True), str(part.get_content_charset()), "ignore")

  def tracta_subject(self):
    subject=self.msg['Subject']
    resultat=""
    fragments=decode_header(subject)
    for fragment in fragments:
      if fragment[1]==None:
	resultat+=fragment[0]
      else:
        resultat+=" "+fragment[0].decode(fragment[1])
    self.subject=resultat


  def enviat_per(self,persona):
    return self.get_from()==persona['emailPreferent'].lower()

  def get_from(self):
    email=parseaddr(self.msg['From'])[1]
    return email.lower()

  def get_to(self):
    email=parseaddr(self.msg['To'])[1]
    return email.lower()

  def get_subject(self):
    return self.subject

  def get_subject_ascii(self):
    return self.subject.encode('ascii','ignore')

  def get_body(self):
    return self.body


  def text2html(self,text):
    # Aquestes 2 linies no fan res perque acaben amb < i > igualment
    #text=text.replace('<','&lt;')
    #text=text.replace('>','&gt;')
    return "<br>\n".join(text.split("\n"))

  def get_attachments(self):
    attachments=[]
    if self.msg.is_multipart():
      parts=self.msg.get_payload()
      i=0
      for part in self.msg.walk():        
        logger.debug("Part: %s" % part.get_content_type())
	i=i+1
        if (i>self.part_body):
          attachments.append(part)
    return attachments

  def te_attachments(self):
    return len(self.get_attachments())>0

