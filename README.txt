MailToTicket v0.1

Aquest programa permet convertir un mails en tickets o comentaris de tickets de gn6
______________________________________________________________________________________________________________________
Estructura

El programa esta fet en python i utilitza els serveis SOA de la UPC de Identitat Digital i de gn6 amb la llibreria suds
També es connecta a LDAP (via script extern) perque SOA no ens proporciona una forma d'obtenir el cn a partir del mail.

Funciona conjuntament amb el sistema de filtre de mails maildrop

______________________________________________________________________________________________________________________
Configuració

S'ha de crear el settings.py a partir del settings-sample.py, on hi ha els següents parametres

username_soa='xxx'
password_soa='xxx'
username_gn6='xxx'
password_gn6='xxx'

domini=1001 #Aquest es de la FIB, posar el que toqui

#Fitxer de log
log_file="/tmp/mailtoticket.log"

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
  "pic\d+.jpg"  # Signatures del notes
]

______________________________________________________________________________________________________________________
Instalació a la bustia

La idea es que mailtoticket funcionarà com un filtre de maildrop. 
La configuració d'aquest filtre serà d'aquest estil (fitxer .mailfilter)
Haurem de configurar on està el script mailtoticket.py i d'altres paràmetres

MAILBOX= "$HOME/nsmail" 
logfile "/tmp/maildrop.log" 
log "Inicio log maildrop" 
log $SHELL
SHELL= "/bin/bash" 
log $SHELL
log $DEFAULT
VERBOSE= 5
MARK=afd25dad494b9345fa2e0a34dc2aa4c11594c3e7b672f772a7fa003ad80bd09f045a170213ae2ba4f47eb8043ac61a56e44ff031a014b82f7508bc5543960138

RESPALDO= "Backup" 
PROCESADO= "Processat" 
NOPROCESADO= "INBOX" 

log "Copia de seguridad en $RESPALDO" 
cc "| /home/soft/bin/dmail +nsmail/$RESPALDO" 

xfilter "/home2/users/lcfib/lcfib-proves/mailtoticket/mailtoticket.py" 

log "Filtro java ejecutado" 

if (/$MARK/)
{
        log "El mensaje ha sido marcado" 
        EXITCODE= 0
        to "| /home/soft/bin/dmail +nsmail/$PROCESADO" 
        exception {
                log "Error en la entrega del mensaje a $PROCESADO" 
        }
}
log "El mensaje no ha sido marcado" 
EXITCODE= 0
to "| /home/soft/bin/dmail +nsmail/$NOPROCESADO" 

______________________________________________________________________________________________________________________
busca_mail.sh

L'exemple que hi ha va contra el LDAP de la FIB. Hauria de ser trivial migrar-lo al LDAP general

______________________________________________________________________________________________________________________
Funcionament del MailToTicket

* mailtoticket.py haurà d'escriure el mail per la sortida estàndard perque funcioni
* mailtoticket.py haurà d'escriure una capçalera amb la marca si el mail s'ha tractat per aixi comunicar al filtre que l'ha processat

Si es compleix aixo, el filtre farà una copia, executarà el filtre i si ha anat bé deixarà el mail a Processat i sino, el deixarà al inbox com si no hagués passat res

MailToTicket actualment es capaç de tractar attachments, fins i tot els que estan "inline" amb el mail i no provenen d'un fitxer. De totes formes, el tractaments
dels attachments es bastant experimental i segur que podem trobar fallos

______________________________________________________________________________________________________________________
Filtres

La idea del programa es executar una sèrie de filtres contra el mail d'entrada, que permetran detectar diferents tipus de mail que tindran
diferents tractaments.

Filtre de Reply

    * Tracta reply a mails, assegurant-nos que segueixen un cert patró d'on podem obtenir el id de ticket
    * Haurà d'existir l'adreça des de la que envien el mail
    * No afegim comentaris a tickets tancats (es el comportament per defecte de la API). Per ara sera el dispatcher qui decidirà si val la pena reobrir
    * TODO: podriem fer que si no reconeixem l'adreça, sigui un mail del solicitant

Filtre de Nou

    * Tracta mails nous.
    * Han de tenir una adreça coneguda
    * Podem fer que certes adreces desti crein els tickets amb diferents parametres, per configuració

Podriem afegir mes filtres detectant per exemple certes paraules claus per fer que els tickets ja quedin automàticament classificats o per exemple reply a tickets tancats que implementin
reobrir el ticket en certs casos (quan no siguin per exemple agraiments...). La llista es llarga!

______________________________________________________________________________________________________________________
Testing

si executem

python -m test.test

El programa passa testos amb alguns mails de proves, fent mocking dels serveis SOA per no crear tickets, pero son bastant incomplets i caldria fer un testeig molt mes exhaustiu