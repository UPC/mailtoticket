#!/bin/bash
echo "Mailtoticket has been started"

# Setup a cron schedule
echo "MAILTO=mailtoticket@unitat.upc.edu
*/5 * * * *  /usr/bin/fetchmail --silent
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f