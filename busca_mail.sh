#!/bin/sh
# Script que donat un mail busca a quin usuari UPC correspon
# Busca com a mail i com a forward (per aixi tenir mes mails d'estudiants)
# Tambe busca com mails @upc.edu agafant la primera part del mail per veure si es directament un username encara que tingui un altre mail
source "/home2/users/lcfib/lcfib-proves/mailtoticket/env.sh"
possible_username=`echo $1 | sed -e 's/@upc.edu//'`
ldapsearch -x -h ldap1.fib.upc.es -p 9388 -b "dc=FIB" -w ${ldap_password} -D "${ldap_username}" "(|(mail=$1)(forward=$1)(uid-web=${possible_username}))" | grep "^uid-web:" | cut -d" " -f2
