#!/usr/bin/python

from suds.wsse import *
from suds.client import Client
import settings

class SOAService:

  username_soa=settings.username_soa
  password_soa=settings.password_soa

  def __init__(self):
    self.client=Client(self.url)
    security = Security()
    security.tokens.append(UsernameToken(self.username_soa,self.password_soa))
    self.client.set_options(wsse=security)

