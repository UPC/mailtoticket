import logging

settings={
  "username_soa":"xxx",
  "password_soa":"xxx",
  "username_gn6":"xxx",
  "password_gn6":"xxx",
  "busca_mail":"/home2/users/lcfib/lcfib-proves/mailtoticket/busca_mail.sh",

  "domini":1001,
  "equip_resolutor_nous":"28510",
  "valors_defecte":{
    "webmaster-proves@fib.upc.edu": {"equipResolutor":"55633"}
  },

  "log_file":"/tmp/mailtoticket.log",
  "log_level":logging.DEBUG,

  "filtres":[
    "filtres.reply.FiltreReply",
    "filtres.nou.FiltreNou",
  ],

  "regex_reply":".*?R[eE]:.*?\[Suport FIB\].*?([\d]+)",

  "mails_addicionals":{
      "tga@fib.upc.edu":"carme.alcala",
      "eva@fib.upc.edu":"eva.salvador",
      "miquel@fib.upc.edu":"miquel.rodriguez",
      "laura@fib.upc.edu":"laura.palanca",
      "laurap@fib.upc.edu":"laura.palanca",
      "lectura.pfc@fib.upc.edu":"laura.palanca",
      "gestio.pfc@fib.upc.edu":"laura.palanca",
      "inscripcio.pfc@fib.upc.edu":"laura.palanca",
      "vd.promocio@fib.upc.edu":"fib.vd.promocio",
      "vd.estudiantat@fib.upc.edu":"fib.vd.estudiantat",
      "vd.postgrau@fib.upc.edu":"fib.vd.postgrau",
      "vd.innovacio@fib.upc.edu":"fib.vd.innovacio",
      "vd.empreses@fib.upc.edu":"fib.vd.empreses",
      "vd.internacionals@fib.upc.edu":"fib.vd.internacionals",
      "vd.iirr@fib.upc.edu":"fib.vd.iirr",
      "cap.estudis@fib.upc.edu":"fib.cap.estudis",
      "cap.estudis.fi@fib.upc.edu":"fib.cap.estudis.fi",
      "brenot@fib.upc.edu":"christine.brenot"
  },

  "filtrar_attachments_per_nom":[
    "paic\d+.jpg"
  ],
  "filtrar_attachments_per_hash":[
    "76f6a359e98f9e0effc214033373b9cf",
    "7526d0f3f7864090353c181158b218c3"
  ]
}
