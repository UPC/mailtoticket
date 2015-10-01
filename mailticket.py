import email
import hashlib
import base64
import re
from email.header import decode_header
from email.utils import parseaddr
import settings

import logging
logger = logging.getLogger(__name__)

class MailTicket:
  """ Classe que encapsula un mail que es convertira en un ticket """

  def __init__(self,file):
    self.filtrar_attachments_per_nom=settings.get("filtrar_attachments_per_nom")
    self.filtrar_attachments_per_hash=settings.get("filtrar_attachments_per_hash")
    self.mails_no_ticket=settings.get("mails_no_ticket")

    self.msg = email.message_from_file(file)
    # Farem lazy initialization d'aquestes 2 properties per si hi ha algun error
    self.body=None
    self.subject=None

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
        if part.get_content_type() in ['text/html']:
          self.body=self.codifica(part)
          break
        if part.get_content_type() in ['text/plain'] and not el_body_es_html:
          body=self.codifica(part)
          self.body=self.text2html(body)
          break

  def codifica(self,part):
    if part.get_content_charset()!=None:
      s=unicode(part.get_payload(decode=True), part.get_content_charset(), "ignore")
    else:
      s=unicode(part.get_payload(decode=True))
    # Aixo es perque pot haver-hi caracters no imprimibles que s'han de filtrar. 
    # Nomes admetem els salts de linia, tabuladors i a partir del 32
    return "".join([x if ord(x)==9 or ord(x)==10 or ord(x)==13 or ord(x)>=32 else '' for x in s])

  def nomes_ascii(self,s):    
    return "".join([x if ord(x)==9 or ord(x)==10 or ord(x)==13 or (ord(x)>=32 and ord(x)<=128) else '' for x in s])

  def tracta_subject(self):
    subject=self.msg['Subject']
    if subject==None:
      self.subject=u""
      return
    resultat=u""
    fragments=decode_header(subject)
    for fragment in fragments:
      if fragment[1]==None:
        resultat+=self.nomes_ascii(fragment[0])
      else:
        resultat+=" "+fragment[0].decode(fragment[1])
    self.subject=resultat.replace('\n', ' ').replace('\r', '')


  def enviat_per(self,persona):
    return self.get_from()==persona['emailPreferent'].lower()

  def get_from(self):
    email=parseaddr(self.msg['From'])[1]
    if len(email)==0: return None
    return email.lower()

  def get_reply_to(self):
    email=parseaddr(self.msg['Reply-To'])[1]
    if len(email)==0: return None
    return email.lower()
	
  def get_uid(self):
    uid=None
    m = re.match("(.*)@est.fib.upc.edu",self.get_from())
    if m:
      return m.group(1)	  
    try:
      uid=self.msg['X-TiquetsGN6'].lower().split('/')[0].split("=")[1].replace(" ",".")
    finally:
      return uid

  def get_to(self):
    to=parseaddr(self.msg['To'])[1]
    try:
      email=parseaddr(self.msg['Resent-To'])[1]
      if email==None or len(email)==0:
        email=to
    except:
        email=to
    finally:
        return email.lower()

  def get_subject(self):
    if self.subject==None:
      self.tracta_subject()
    return self.subject

  def get_subject_ascii(self):
    return self.get_subject().encode('ascii','ignore')

  def get_body(self):
    if self.body==None:
      self.tracta_body()
    return self.body


  def text2html(self,text):
    text=text.replace("<","&lt;")
    text=text.replace(">","&gt;")
    return "<br>\n".join(text.split("\n"))

  def get_attachments(self):
    if self.body==None:
      self.tracta_body()
    attachments=[]
    if self.msg.is_multipart():
      parts=self.msg.get_payload()
      i=0
      for part in self.msg.walk():        
        logger.debug("Part: %s" % part.get_content_type())
        i=i+1
        if (i>self.part_body) and self.comprovar_attachment_valid(part):
          attachments.append(part)
    return attachments

  def comprovar_attachment_valid(self,attachment):
    ctype=attachment.get_content_type()
    filename=attachment.get_filename()
    contingut=attachment.get_payload()

    valid=False
    # Si no tenim filename, nomes pot ser una imatge incrustada
    if filename==None:
      if ctype not in ['image/jpeg','image/png','image/gif']:
        return False
    # I si tenim filename, que no sigui un dels que filtrem
    else:
      for f in self.filtrar_attachments_per_nom:
        p=re.compile(f)
        if p.match(filename):
          return False

    # Si es molt llarg es valid segur, no sera una signatura!
    if len(contingut)>1000000:
      return True

    # Segona part: mirem que no sigui un fitxer prohibit per hash

    hash=hashlib.md5(base64.b64decode(contingut)).hexdigest()
    logger.info("Hash:"+hash)
    return hash not in self.filtrar_attachments_per_hash

  def te_attachments(self):
    return len(self.get_attachments())>0
	
  def cal_tractar(self):
    if self.get_from() in self.mails_no_ticket: return False
    if self.msg.get_content_type()=="multipart/report": return False
    if "Return Receipt" in self.get_body(): return False
    if "DELIVERY FAILURE" in self.get_subject(): return False
    return True

  def __str__(self):
    return self.msg.__str__()
