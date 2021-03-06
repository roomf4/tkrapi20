#!/bin/bash

# pgcopy2heroku.bash

# This script should copy some data to heroku postgres.

# export HPGURL=postgres://hpgygqtixbpwjf:70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab@ec2-54-163-233-201.compute-1.amazonaws.com:5432/d2nebmdp327bn5

# pg_dump --no-owner -W -h 127.0.0.1 -d tkrapi -U tkrapi \
#           --no-tablespaces -t tkrprices -t predictions -t features \
#           --no-owner -f /tmp/pgdump.sql

pg_dump --dbname=${PGURL}    \
	--no-owner --no-tablespaces \
	-t tkrprices -t predictions -t features \
        -f /tmp/pgdump.sql

psql --dbname=${HPGURL} <<EOF
drop table tkrprices;
drop table features;
drop table predictions;
EOF

psql --dbname=${HPGURL} -f /tmp/pgdump.sql

exit
