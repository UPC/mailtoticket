
v4.0.0 / 2022-04-13
===================

## Canvis importants

  * Ha canviat la dependència de suds-jarko per suds-community (haureu d'actualitzar la instal·lació local)

## Millores

  * Nou paràmetre `mails_sempre_ticket`
  * Nou paràmetre `afegir_solicitants_addicionals` indicats al Cc (cal la versió 6 de l'API de GN6)
  * Nou paràmetre `no_escriure_sortida`
  * Motor de regles amb capçaleres multivaluades
  * La guia ràpida en format markdown

## Bugs resolts

  * Neteja dels correus citats a Gmail
  * Comprovació de literals amb `==`
  * Comprovació d'existència de capçalera al motor de regles
  * Nom filtre `reply_reobrint` a `settings_sample.py`
  * Avís sobre `assertEquals`
  * Propaga els errors del bus per evitar crear tiquets nous en lloc d'afegir comentaris o adjunts

v3.1.0 / 2021-07-09
===================

## Canvis

  * Als usuaris externs ja no se'ls envia notificació de creació de tiquet (#211)
  * Ara també s'intenta resoldre l'usuari de correus genèrics mitjançant el servei d'Identitat Digital (#206)
  * La capçalera dels missatges generats per MailToTicket inclou també l'adreça de destinació del correu (#210)

## Bugs resolts

  * Bug: s'ha fet més robust el procés de codificació dels attachments per a alguns casos #214

