from bs4 import BeautifulSoup
import bleach
import re

def neteja(html):
  html=sanitize(html)
  html=treure_reply(html)
  html=treure_signatura(html)
  return html

def sanitize(html):
  # Mails del tipus <mail@fib.upc.edu> no son tags!
  #html=re.sub("<([^ ]*@[^ ]*)>",r"&gt;\1&lt;",html)
  return bleach.clean(html,
    tags=[
      'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
      'strong', 'ul','pre','table','tr','td','th','tbody','thead','tfoot','div','br','hr','img','p'
    ],
    attributes={
      '*':['class'],
      'img':['src'],
      'a':['href'],
      'td':['colspan','rowspan'],
      'blockquote':['type']
    },
    strip=True
  )

def treure_reply(html):
  html=treure_blockquote(html)
  html=treure_reply_text(html)
  return html

def treure_blockquote(html):
  soup = BeautifulSoup(html,"html.parser")

  tags = soup.select('blockquote[type=cite]')
  if len(tags)==1: tags[0].decompose()

  tags = soup.select('div .moz-cite-prefix')
  if len(tags)==1: tags[0].decompose()

  return str(soup)

def treure_reply_text(text):
  blocs=0;
  anterior=False
  linies=text.split("<br>\n")
  sensequotes=[]
  for l in linies:
    if l.startswith("&gt;"):
      dintre=True
      if anterior!=dintre: blocs+=1
    else:
      dintre=False
      sensequotes.append(l)
    anterior=dintre
  if blocs==1:
    return "<br>\n".join(sensequotes)
  else:
    return text

def treure_signatura(html):
  html=treure_signatura_text(html)
  html=treure_signatura_html(html)
  return html

def treure_signatura_text(text):
  blocs=0;
  signatura=False
  cos=[]
  linies=text.split("<br>\n")
  for l in linies:
    if re.match("^--[\s]+$",l):
      signatura=True
      blocs+=1
    if not signatura:
      cos.append(l)
  if blocs==1:
    return "<br>\n".join(cos)
  else:
    return text

def treure_signatura_html(html):
  soup = BeautifulSoup(html,"html.parser")
  tags = soup.select('.moz-signature')
  if len(tags)==1: tags[0].decompose()
  return str(soup)

def treure_pgp(text):
  pgp=False
  cos=[]
  linies=text.split("\n")
  for l in linies:
    if re.match("^-----BEGIN PGP PUBLIC KEY BLOCK-----$",l):
      pgp=True
    if not pgp:
      cos.append(l)
    if re.match("^-----END PGP PUBLIC KEY BLOCK-----$",l):
      pgp=False
  return "\n".join(cos)
