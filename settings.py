# Configuracio del mailtoticket

username_soa='xxx'
password_soa='xxx'
username_gn6='xxx'
password_gn6='xxx'
domini=1001

# Logging
import logging
log_file="/tmp/mailtoticket.log"
log_level=logging.DEBUG

# Script per buscar mail a ldap
busca_mail="/home2/users/lcfib/lcfib-proves/mailtoticket/busca_mail.sh"

# Expressio regular per extreure el numero de ticket
regex_reply=".*?R[eE]:.*?\[Suport FIB\].*?([\d]+)"

# Equip on creem els tickets per defecte (o sigui, l'equip "dispatcher")
equip_resolutor_nous="28510"

# Valors per defecte segons mail desti
# No nomes podem canviar l'equip resolutor. Tambe prioritat, assignacio...
valors_defecte={}
valors_defecte['webmaster-proves@fib.upc.edu']= {'equipResolutor':'28513'}

# Mails addicionals que no estan a LDAP... pero que poden enviar tickets

mails_addicionals={
  "tga@fib.upc.edu":"carme.alcala",
  "lectura.pfc@fib.upc.edu":"laura.palanca"
}

filtrar_attachments=[
  "pic\d+.jpg"	# Signatures del notes
]

