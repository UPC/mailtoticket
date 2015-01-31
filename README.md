MailToTicket
============

Una pasarel·la de correu per al gestor de tiquets GN6.

Estructura
----------

El programa esta fet en python i utilitza els serveis SOA de la UPC de Identitat Digital i de gn6 amb la llibreria suds
També es connecta a LDAP (via script extern) perque SOA no ens proporciona una forma d'obtenir el cn a partir del mail.

Funciona conjuntament amb el sistema de filtre de mails maildrop

Configuració
------------

S'ha de crear el settings.json a partir del settings.json.sampls, on hi ha els següents parametres
 ```
{
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

  "log_file":"/tmp/mailtoticket.log",
  "log_level":"logging.DEBUG",

  "filtres":[
    "filtres.reply.FiltreReply",
    "filtres.nou.FiltreNou"
  ],

  "regex_reply":".*?R[eE]:.*?\\[Suport FIB\\].*?([\\d]+)",

  "mails_addicionals":{
      "gestio.pfc@fib.upc.edu":"laura.palanca",
      "cap.estudis@fib.upc.edu":"fib.cap.estudis",
  },

  "filtrar_attachments_per_nom":[
    "paic\\d+.jpg"
  ],

  "filtrar_attachments_per_hash":[
    "76f6a359e98f9e0effc214033373b9cf",
    "7526d0f3f7864090353c181158b218c3"
  ]
}
 ```
Instalació a la bustia
----------------------

La idea es que mailtoticket funcionarà com un filtre de maildrop. 
La configuració d'aquest filtre serà d'aquest estil (fitxer .mailfilter)
Haurem de configurar on està el script mailtoticket.py i d'altres paràmetres
 ```
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

log "Copia de seguretat a $RESPALDO" 
cc "| /home/soft/bin/dmail +nsmail/$RESPALDO" 

xfilter "/path/to/mailtoticket/mailtoticket.py" 

log "MailToTicket executat" 

if (/$MARK/)
{
        log "Missatge processat" 
        EXITCODE= 0
        to "| /home/soft/bin/dmail +nsmail/$PROCESADO" 
        exception {
                log "Error guardant el missatge a $PROCESADO" 
        }
}
log "El mensaje no processat" 
EXITCODE= 0
to "| /home/soft/bin/dmail +nsmail/$NOPROCESADO" 
 ```

busca_mail.sh
-------------

L'exemple que hi ha va contra el LDAP de la FIB. Hauria de ser trivial migrar-lo al LDAP general


Funcionament del MailToTicket
-----------------------------

* mailtoticket.py haurà d'escriure el mail per la sortida estàndard perque funcioni
* mailtoticket.py haurà d'escriure una capçalera amb la marca si el mail s'ha tractat per aixi comunicar al filtre que l'ha processat

Si es compleix aixo, el filtre farà una copia, executarà el filtre i si ha anat bé deixarà el mail a Processat i sino, el deixarà al inbox com si no hagués passat res


Filtres
-------

La idea del programa es executar una sèrie de filtres contra el mail d'entrada, que permetran detectar diferents tipus de mail que tindran
diferents tractaments.

Filtre de Reply

    * Tracta reply a mails, assegurant-nos que segueixen un cert patró d'on podem obtenir el id de ticket
    * Si l'adreça des de la que envien el mail es coneguda, crea el ticket en nom seu. Si no, en nom del solicitant
    * No afegim comentaris a tickets tancats (es el comportament per defecte de la API).

Filtre de Nou

    * Tracta mails nous que s'han de crear com a nous tickets
    * Han de tenir una adreça coneguda
    * Podem fer que certes adreces desti (alias que van a parar al mateixa bustia) crein els tickets amb diferents parametres, per configuració

Podriem afegir mes filtres detectant per exemple certes paraules claus per fer que els tickets ja quedin automàticament classificats o per exemple reply a tickets tancats que implementin reobrir el ticket en certs casos (quan no siguin per exemple agraiments...). La llista es llarga!

Testing
-------

si executem

python -m test.test

El programa passa testos amb alguns mails de proves, fent mocking dels serveis SOA per no crear tickets, pero son bastant incomplets i caldria fer un testeig molt mes exhaustiu
