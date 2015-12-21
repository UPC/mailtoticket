#!/bin/sh
#
# Wrapper to run mailtoticket.py and fix the outgoing message format
# before injecting it to sendmail:
#
# * Remove the second line which breaks RFC822
# * Remove Message-Id header so sendmail builds a new one.
#   Reusing an existing Message-Id is a Very Bad Idea (e.g.
#   Cyrus IMAP server may ignore duplicates).
#

SENDMAIL_CMD=/usr/sbin/sendmail
MAILTOTICKET_DIR=$HOME/mailtoticket

set -e
exec >> $0.log 2>&1

cd "$MAILTOTICKET_DIR"
python mailtoticket.py \
| sed -e '2d' -e '0,/^[Mm]essage-[Ii][Dd]:/{//d}' \
| $SENDMAIL_CMD -oem -i -t
EXIT_CODE=$?

echo "$(date '+%Y-%m-%d %H:%M:%S') exit status=${EXIT_CODE}"
