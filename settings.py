"""
El modul de settings s'importa i s'accedeix als valors amb settings.get("clau")
Abans d'accedir podem carregar la configuracio o agafara la per defecte
"""

def load(module="settings_default"):
  global settings
  m=__import__(module,"settings")
  settings=m.settings
#  from settings_sample import settings
#  print settings['domini']

def load1():
  global settings
  from settings_default import settings

def get(clau):
  global settings  
  try:
    return settings[clau]
  except:
    load()
    return settings[clau]
