from suds.wsse import *
from suds.client import Client
import settings

class SOAService(object):

  def __init__(self):
    self.username_soa=settings.get("username_soa")
    self.password_soa=settings.get("password_soa")
    self.client=Client(self.url)
    security = Security()
    security.tokens.append(UsernameToken(self.username_soa,self.password_soa))
    self.client.set_options(wsse=security)

