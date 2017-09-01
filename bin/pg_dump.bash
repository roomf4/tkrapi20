#!/bin/bash

# pg_dump.bash

# This script should create a pg-dump file.

# pg_dump --help

PGPASSWORD=tkrapi pg_dump --no-owner -W -h 127.0.0.1 -d tkrapi -U tkrapi --no-tablespaces -t tkrprices --no-owner  -f /tmp/pgdump.sql

exit
