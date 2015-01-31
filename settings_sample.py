import logging
import tempfile

settings={
  "username_soa":"xxx",
  "password_soa":"xxx",
  "username_gn6":"xxx",
  "password_gn6":"xxx",
  "busca_mail":"/path/to/busca_mail.sh",

  "domini":999,
  "equip_resolutor_nous":"99999",
  "valors_defecte":{
    "webmaster@meudomini.upc.edu": {"equipResolutor":"11111"}
  },

  "log_file":tempfile.gettempdir()+"/mailtoticket.log",
  "log_level":logging.DEBUG,

  "filtres":[
    "filtres.reply.FiltreReply",
    "filtres.nou.FiltreNou"
  ],

  "regex_reply":".*?R[eE]:.*?\[Suport FIB\].*?([\d]+)",

  "mails_addicionals":{
      "gestio.pfc@fib.upc.edu":"laura.palanca",
      "cap.estudis@fib.upc.edu":"fib.cap.estudis",
  },

  "filtrar_attachments_per_nom":[
    "paic\d+.jpg"
  ],

  "filtrar_attachments_per_hash":[
    "76f6a359e98f9e0effc214033373b9cf",
    "7526d0f3f7864090353c181158b218c3"
  ]
}
