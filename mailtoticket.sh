#!/bin/sh
set -e
exec >> $0.log 2>&1
cd $HOME/mailtoticket
./mailtoticket.py \
| sed -e '2d' -e '0,/^[Mm]essage-[Ii][Dd]:/{//d}' \
| /usr/sbin/sendmail -oem -i -t
EXIT_CODE=$?
echo "$(date '+%Y-%m-%d %H:%M:%S') exit status=${EXIT_CODE}"
