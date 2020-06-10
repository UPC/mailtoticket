# -*- coding: utf-8 -*-
"""
El modul de settings s'importa i s'accedeix als valors amb settings.get("clau")
Abans d'accedir podem carregar la configuracio o agafara la per defecte
"""


def load(module="settings_default"):
    global settings
    try:
        m = __import__(module, "settings")
    except ImportError:
        raise SystemExit('Error! No file with configurations found: settings_default.py')
    except Exception:
        raise SystemExit('Error! File found, but error in settings. Addapt settings_sample.py file to your custom settings_default.py')

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
