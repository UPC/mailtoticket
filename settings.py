"""
El modul de settings s'importa i s'accedeix als valors amb settings.get("clau")
Abans d'accedir podem carregar la configuracio o agafara la per defecte
"""


def load(module="settings_default"):
    global settings
    try:
        m = __import__(module, "settings")
        settings = m.settings
    except Exception:
        settings = {}


def get(clau):
    if 'settings' not in globals():
        load()

    global settings
    try:
        return settings[clau]
    except Exception:
        return None


def set(clau, valor):
    global settings
    settings[clau] = valor


def init():
    global settings
    settings = {}
