from suds.wsse import *
from suds.client import Client
import settings

class SOAService(object):

  username_soa=settings.get("username_soa")
  password_soa=settings.get("password_soa")

  url = "https://bus-soades.upc.edu/GestioIdentitat/Personesv6?wsdl"

  def __init__(self):
    self.client=Client(self.url)
    security = Security()
    security.tokens.append(UsernameToken(self.username_soa,self.password_soa))
    self.client.set_options(wsse=security)

