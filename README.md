MailToTicket
============

Una pasarel·la de correu per al gestor de tiquets GN6.

Estructura
----------

El programa esta fet en python i utilitza els serveis SOA de la UPC de Identitat Digital i de gn6 amb la llibreria suds

Funciona conjuntament amb el sistema de filtre de mails maildrop

Requeriments
------------

* Python (a partir de 2.5)
* Maildrop i, opcionalment, dmail
* Usuari per accedir a gn6 via SOA
* Usuari per accedir al bus SOA
* Accés al servei SOA https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl
* Accés al servei SOA https://bus-soa.upc.edu/gN6/GestioTiquetsv2?wsdl

Configuració
------------

S'ha de crear el _settings_default.py_ a partir del settings_sample.py, on hi ha els següents parametres,
autocomentats

 ```
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

  # Valors amb els que creem els tickets dependent de l'adreça a la qual hem enviat 
  # el mail. A part de l'equipResolutor, es poden canviar tots els paramatres 
  # documentats al servei SOA de creació de tickets (prioritat, tipus...)
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

  # Mails dels que no volem crear ticket per la rao que sigui
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
} 

```

Es poden crear altres filtxers de configuracio que es podran llegir executant mailtoticket.py -c settings_alternatius (sense l'extensio .py)

Instalació a la bustia
----------------------

La idea es que mailtoticket funcionarà com un filtre de maildrop. 
La configuració d'aquest filtre serà d'aquest estil (fitxer .mailfilter)
Haurem de configurar on està el script mailtoticket.py i d'altres paràmetres

Per fer aixo haurem de crear dos fitxers: .forward i .mailfilter. 

* .forward
```
"| /home/soft/maildrop/bin/maildrop -d ${USER}"
```

* .mailfilter
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

Filtre de Reply Reobrint

* Es una extensio del Filtre de Reply
* Reobre els ticket tancats quan s'hi fa reply

Filtre de Nou

* Tracta mails nous que s'han de crear com a nous tickets
* Han de tenir una adreça coneguda
* Podem fer que certes adreces desti (alias que van a parar al mateixa bustia) crein els tickets amb diferents parametres, per configuració

Filtre de Nou Extern

* Es una extensio del Filtre de Nou
* Crea tickets també per usuaris no coneguts amb l'usuari definit al parametre "usuari_extern"


Podriem afegir mes filtres detectant per exemple certes paraules claus per fer que els tickets ja quedin automàticament classificats o per exemple reply a tickets tancats que implementin reobrir el ticket en certs casos (quan no siguin per exemple agraiments...). La llista es llarga!

Testing
-------

si executem

    $ python -m test.test

El programa passa testos amb alguns mails de proves, fent mocking dels serveis SOA per no crear tickets, pero son bastant incomplets i caldria fer un testeig molt mes exhaustiu
