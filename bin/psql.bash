#!/bin/bash

# psql.bash

# This script starts psql for me and connects me to correct host, role and db.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
. ${SCRIPTPATH}/../env.bash
# PGPASSWORD=tkrapi psql -aP pager=no -U tkrapi -h 127.0.0.1 tkrapi $@
# Should be better syntax than above:
psql -aP pager=no --dbname=$PGURL
# Should be useful for look at data on Heroku:
# psql -aP pager=no --dbname=$HPGURL

exit
