#!/bin/bash

# pgcopy2heroku.bash

# This script should copy some data to heroku postgres.

# export HPGURL=postgres://hpgygqtixbpwjf:70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab@ec2-54-163-233-201.compute-1.amazonaws.com:5432/d2nebmdp327bn5

PGPASSWORD=tkrapi
pg_dump --no-owner -W -h 127.0.0.1 -d tkrapi -U tkrapi \
          --no-tablespaces -t tkrprices -t predictions -t features \
          --no-owner -f /tmp/pgdump.sql



PGPASSWORD=70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab \
psql -U hpgygqtixbpwjf -h ec2-54-163-233-201.compute-1.amazonaws.com d2nebmdp327bn5 <<EOF
drop table tkrprices;
drop table features;
drop table predictions;
EOF

PGPASSWORD=70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab \
psql -U hpgygqtixbpwjf \
-h ec2-54-163-233-201.compute-1.amazonaws.com d2nebmdp327bn5 \
-f /tmp/pgdump.sql

exit
