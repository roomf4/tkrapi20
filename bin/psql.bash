#!/bin/bash

# psql.bash

# This script starts psql for me and connects me to correct host, role and db.
. env.bash

# PGPASSWORD=tkrapi psql -aP pager=no -U tkrapi -h 127.0.0.1 tkrapi $@

psql -aP pager=no --dbname=$PGURL

exit
