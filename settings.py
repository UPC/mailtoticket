"""
El modul de settings s'importa i s'accedeix als valors amb settings.get("clau")
Abans d'accedir podem carregar la configuracio o agafara la per defecte
"""

def load(module="settings_default"):
  global settings
  m=__import__(module,"settings")
  settings=m.settings

def get(clau):  
  if not 'settings' in globals():
    load()
  global settings  
  try:
    return settings[clau]
  except:
    return None
