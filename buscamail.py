#!/usr/bin/python
from soa.identitat import GestioIdentitat
import sys

if len(sys.argv) < 2:
    print("Has de posar un mail com a parametre")
    sys.exit()

if __name__ == '__main__':
    mail = sys.argv[1]
    identitat = GestioIdentitat()
    uid = identitat.obtenir_uid(mail)
    print("El username associat a aquest mail es:" + uid)
