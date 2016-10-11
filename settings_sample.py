# -*- coding: utf-8 -*-
import logging
import tempfile
import os

# Utilitzeu això si voleu fer servir diverses instàncies a la mateixa
# maquina. Cada una necessita el seu directori temporal:
#
# tempfile.tempdir = os.environ['HOME'] + "/tmp"

settings = {

    # Usuaris SOA i GN6
    "username_soa": "xxx",
    "password_soa": "xxx",
    "username_gn6": "xxx",
    "password_gn6": "xxx",

    # Instància de GN6 on voleu crear els tiquets
    "domini": "999",

    # Equip resolutor per defecte amb què s'han de crear els tiquets
    "equip_resolutor_nous": "99999",

    # Usuari amb què es crearan els tiquets pels correus desconeguts
    # (únicament si teniu activat el FiltreNouExtern)
    "usuari_extern": "extern.general",

    # Valors amb què es crearan els tiquets dependent de les capçaleres
    # del correu rebut. A part de l'equipResolutor, es poden canviar
    # tots els paramatres documentats al servei SOA de creació de tiquets
    # (prioritat, tipus...)
    "valors_defecte": [
        {
            "order": ['Resent-To', 'To'],
            "match": "^webmaster@unitat\.upc\.edu$",
            "defaults": {"equipResolutor": "11111"}
        },
        {
            "order": ['Resent-From', 'From'],
            "match": "^nom\.cognom@upc\.edu$",
            "defaults": {"equipResolutor": "11113"}
        },
        {
            "order": ['Resent-From'],
            "match": "^nom@unitat\.upc\.edu$",
            "defaults": {"equipResolutor": "11112"}
        },
        {
            "order": ['Subject'],
            "match": ".*URGENT",
            "defaults": {"urgencia": "GRAVETAT_ALTA"}
        }
    ],

    # Es notifiquen al solicitant els comentaris afegits via mailtoticket
    # per algun usuari diferents del propi solicitant? (per defecte, si)
    "notificar_comentaris_afegits": True,

    # Filtres actius. També podem utilitzar:
    # - filtres.reply_reobrint.FiltreRepyReobrint (reobre tiquets tancats)
    # - filtres.nou_extern.FiltreNouExtern (obre tiquets de correus
    #   desconeguts)
    "filtres": [
        "filtres.reply.FiltreReply",
        "filtres.nou.FiltreNou"
    ],

    # Patró per detectar el número de tiquet
    "regex_reply": ".*?R[eEvV]:.*?\[Suport Unitat ([\d]+)\]",

    # Patró per detectar si es tracta d'un comentari privat
    # (també cal modificar la plantilla corresponent a GN6)
    "regex_privat": "(?i)\(comentari privat\)",

    # Correus addicionals propis de cada unitat que no es troben al servei
    # d'Identitat Digital UPC. Per cada correu cal indicar quin usuari li
    # correspon per crear el tiquet.
    "mails_addicionals": {
        "gestio.pfc@escola.upc.edu": "nom.cognom",
        "cap.estudis@escola.upc.edu": "escola.cap.estudis",
    },

    # Patrons de diferents correus que equivalen a un mateix usuari
    # o bé a una referència del propi patró (per exemple, el correu
    # nom.cognom@upc.edu -> nom.cognom).
    "patrons_mail_addicionals": {
        "^root@([a-z0-9.\-]+\.)?unitat\.upc\.e(s|du)$": "extern.general",
        "^(.*)@upc.edu$": "%s",
        "^(.*)@upcnet.es$": "%s"
    },

    # Correus dels que no s'ha de crear cap tiquet per la raó que sigui
    "mails_no_ticket": [
        "info.exemple@upc.edu",
        "^.*@example\.com$",
    ],

    # Filtres d'adjunts que no s'han de processar (per exemple, les
    # signatures que contenen imatges adjuntes). Es poden filtrar
    # pel nom de l'adjunt o per l'emprempta digital en MD5.
    "filtrar_attachments_per_nom": [
        "paic\d+.jpg"
    ],

    "filtrar_attachments_per_hash": [
        "76f6a359e98f9e0effc214033373b9cf",
        "7526d0f3f7864090353c181158b218c3"
    ],

    # Fitxers de log i grau de detall
    "log_file": tempfile.gettempdir() + "/mailtoticket.log",
    "log_level": logging.INFO,

    # Notificació dels informes d'error per correu
    "notificar_errors": True,
    "notificar_errors_from": "mailtoticket@unitat.upc.edu",
    "notificar_errors_to": "nom.cognom@unitat.upc.edu",
    "servidor_mail": "relay.upc.edu"
}
