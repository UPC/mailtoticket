# -*- coding: utf-8 -*-
import logging
import tempfile
import os

# Descomentar això si volem fer servir mailtoticket 
# en diferents comptes a la mateixa maquina
# Deixa els temporals al $HOME/tmp
# 
# tempfile.tempdir=os.environ['HOME']+"/tmp"

settings={

  # Usuaris SOA i gn6
  "username_soa":"xxx",
  "password_soa":"xxx",
  "username_gn6":"xxx",
  "password_gn6":"xxx",

  # Instància de gn6 on volem crear els tickets
  "domini":999,

  # ID de l'equip resolutor per defecte on s'han de crear els tickets
  "equip_resolutor_nous":"99999",

  # ID de l'usuari al qual es crearan els tickets d'usuaris dels que no tenim el mail
  # (unicament si fem servir el filtre FiltreNouExtern)
  "usuari_extern":"11763",

  # Valors amb els que creem els tickets dependent de l'adreça a la qual hem enviat el mail
  # A part de l'equipResolutor, es poden canviar tots els paramatres documentats al servei
  # SOA de creació de tickets (prioritat, tipus...)
  "valors_defecte":{
    "webmaster@meudomini.upc.edu": {"equipResolutor":"11111"}
  },

  # Filtrs actius. També podem utilitzar 
  # - filtres.reply_reobrint.FiltreRepyReobrint (que reobre tickets tancats)
  # - filtres.nou_extern.FiltreNouExtern (que obre tickets d'usuaris desconeguts)
  "filtres":[
    "filtres.reply.FiltreReply",
    "filtres.nou.FiltreNou"
  ],

  # Patrons per detectar el número de ticket i si un ticket es un comentari intern
  # Pel comentari intern, s'ha de tocar la plantilla a gn6 per afegir-ho
  "regex_reply":".*?R[eE]:.*?\[Suport FIB\].*?([\d]+)",
  "regex_privat":".*\(Comentari intern\)",

  # Mails addicionals propis de cada unitat, que no podem trobar a Identitat Digital
  # Per cada mail, diem a nom de quin usuari s'han de crear els tickets
  "mails_addicionals":{
    "gestio.pfc@fib.upc.edu":"laura.palanca",
    "cap.estudis@fib.upc.edu":"fib.cap.estudis",
  },

  # Patrons de mail que equivalen a un usuari concret o be 
  # a una backreference del patro (ex: jaume.moral@upc.edu -> jaume.moral)
  "patrons_mail_addicionals": {
    "^root@(.*).fib.upc.es$":"usuari.generic",
    "^(.*)@upc.edu$":"%s",
    "^(.*)@upcnet.es$":"%s"
  },

  # Mails dels que no volem crear ticket per la raó que sigui
  "mails_no_ticket":[
    "cursos.slt@upc.edu"
  ],

  # Filtres d'attachments que no volem processar (típicament signatures)
  "filtrar_attachments_per_nom":[
    "paic\d+.jpg"
  ],
  "filtrar_attachments_per_hash":[
    "76f6a359e98f9e0effc214033373b9cf",
    "7526d0f3f7864090353c181158b218c3"
  ],

  # Fitxers de log
  "log_file":tempfile.gettempdir()+"/mailtoticket.log",
  "log_level":logging.INFO,

  # Mails de notificació quan no es pot tractar el ticket
  "notificar_errors":True,
  "notificar_errors_from":"mailtoticket@upc.edu",
  "notificar_errors_to":"jaumem@fib.upc.edu",
  "servidor_mail":"mail.fib.upc.edu"
} 
