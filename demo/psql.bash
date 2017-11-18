#!/bin/bash

# psql.bash

# This script demos how to start psql for me and connect me to correct host, role and db.

# Below, I list syntax I used to create role tkrapi and database tkrapi:
# sudo su - postgres
# psql
# CREATE ROLE tkrapi with login superuser password 'tkrapi';
# CREATE DATABASE tkrapi;

cd ~/tkrapi20/demo/
. ../env.bash
# Here is one way to do it:
# PGPASSWORD=tkrapi psql -aP pager=no -U tkrapi -h 127.0.0.1 tkrapi $@
# This should be better syntax than above:
psql -aP pager=no --dbname=$PGURL $@
# Should be useful to see data on Heroku:
# psql -aP pager=no --dbname=$HPGURL $@

exit
