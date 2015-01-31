import json

def load_settings(file="settings.json"):
  global settings
  json_data=open(file)
  settings = json.load(json_data)
  json_data.close()

try:
  settings
except:
  load_settings()

