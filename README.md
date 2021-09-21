MailToTicket
============

Una pasarel·la de correu per al gestor de tiquets GN6.

La documentació del servei està disponible a la web de [Serveis TIC](https://serveistic.upc.edu/ca/atic/documentacio/mailtoticket-convertir-un-mail-en-un-tiquet).

Per tenir una idea més precisa dels objectius d'aquest projecte, vegeu la [presentació del projecte](http://www.slideshare.net/angelaguilera/mailtoticket-presentaci-final-de-projecte) a la jornada de tancament Nexus24.

![Build Status (GH Actions)](https://github.com/UPC/mailtoticket/actions/workflows/python-app.yml/badge.svg)
[![Build Status (Travis CI)](https://travis-ci.com/UPC/mailtoticket.svg?branch=master)](https://travis-ci.com/UPC/mailtoticket)
[![Issue Count](https://codeclimate.com/github/UPC/mailtoticket/badges/issue_count.svg)](https://codeclimate.com/github/UPC/mailtoticket)

Requisits
---------

Aquest programa necessita els següents serveis SOA de la UPC:

*   [Identitat Digital](https://bus-soa.upc.edu/GestioIdentitat/Personesv6?wsdl): permet identificar els sol·licitants amb el correu
*   [GN6](https://bus-soa.upc.edu/gN6/GestioTiquetsv2?wsdl): permet gestionar els tiquets

Us caldrà disposar d'un usuari i contrasenya per accedir al bus SOA.
L'usuari i contrasenya del servei GN6 els podeu definir a la vostra instància.

El llenguatge de programació triat és Python 3, vegeu el fitxer de [dependències](requirements.txt).

Per poder utilitzar aquest programa necessitareu configurar un _Mail Delivery Agent_ (MDA) al vostre servidor de correu o a la bústia IMAP corresponent.

Instal·lació
------------

La forma recomanada d'instal·lació és dins d'un _virtualenv_ de Python 3 per poder gestionar les dependències sense permisos d'administrador:

```
git clone https://github.com/UPC/mailtoticket.git
cd mailtoticket
virtualenv local -p python3
echo "PATH=$PWD/local/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
sudo apt-get install build-essential libpython3-dev libsasl2-dev libldap2-dev
pip install -r requirements.txt
```
Dockerització (pilot)
---------------------

```
docker build . -t mailtoticket
cat missatge.txt | docker run -v /path/to/settings_default.py:/usr/src/app/settings_default.py:ro --rm -i mailtoticket
```


Configuració de la bústia
-------------------------

El programa funciona com un filtre de correu i s'ha d'executar per cada correu que es vulgui processar mitjançant un MDA.
Podeu utilitzar MDA coneguts com ara maildrop o procmail. Vegeu els exemples documentats al wiki.

Configuració de la instància
----------------------------

Heu de crear el fitxer `settings_default.py` a partir del [settings_sample.py](settings_sample.py) per configurar la vostra instància.

Si voleu tenir diferents instàncies del programa, podeu crear fitxers de configuració amb noms diferents.
Per llegir-los només cal que ho indiqueu amb l'opció `-c` tot indicant el nom del fitxer sense l'extensió .py:

```
cat correu.txt | python mailtoticket.py -c settings_alternatius
```

Filtres i accions
-----------------

El comportament del programa és executar una sèrie de filtres sobre el correu d'entrada que permetran triar diferents tipus d'accions a realitzar.

*   **Resposta**
    *   Tracta les respostes dels tiquets, comprovant que segueixen un cert patró d'on es pot obtenir el número del tiquet.
    *   Si l'adreça remitent del correu és coneguda, s'afegeix un comentari en nom seu. Altrament en nom del sol·licitant.
    *   No s'afegeixen comentaris als tiquets tancats (és el comportament per defecte del servei de GN6).
*   **Resposta Reobrint**
    *   Reobre els tiquets tancats quan s'hi rep un resposta si està dins el termini establert pel servei.
    *   És una extensió del filtre **Resposta**.
*   **Nou**
    *   Tracta els correus que s'han de processar com a nous tiquets.
    *   Han de tenir una adreça remitent coneguda.
    *   Es pot configurar la creació dels tiquets amb paràmetres diferents (per exemple, l'equip resolutor) segons el valor de determinades capçaleres de correu.
*   **Nou Extern**
    *   Crea tiquets per adreces desconegudes amb un usuari predeterminat per configuració.
    *   És una extensió del filtre **Nou**.

Opcional
--------

És pot configurar una tercera font de dades per comprovar si existeix una adreça en un LDAP extern. Per fer-ho cal afegir al fitxer `settings_default.py` al diccionari de settings la següent configuració:

```
settings = {

    ...
    # LDAP Extern config
    "LDAP_SERVER_URL": "xxx",
    "LDAP_BIND_USER": "xxx",
    "LDAP_PASSWORD": "xxx",
    "LDAP_BASE_SEARCH": "xxx",
    ...
}
```

Llicència
---------

Copyright (C) 2015-2020 Universitat Politècnica de Catalunya - UPC BarcelonaTech - www.upc.edu

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
