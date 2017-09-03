#!/bin/bash

# hpsql.bash

# This script should run psql against heroku postgres.

# export HPGURL=postgres://hpgygqtixbpwjf:70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab@ec2-54-163-233-201.compute-1.amazonaws.com:5432/d2nebmdp327bn5

# PGPASSWORD=70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab psql -aP pager=no -U hpgygqtixbpwjf  -h ec2-54-163-233-201.compute-1.amazonaws.com d2nebmdp327bn5 $@

psql -aP pager=no --dbname=$HPGURL

exit

