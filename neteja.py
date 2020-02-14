#!/usr/bin/python
from mailticket import MailTicket
from filtres.netejar import FiltreNou
import sys

if __name__ == '__main__':
    mail = MailTicket(sys.stdin)
    netejat = FiltreNou(mail).filtrar()
    print netejat.encode('utf-8')
