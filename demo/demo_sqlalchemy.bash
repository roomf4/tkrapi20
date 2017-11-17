#!/bin/bash

# ~/tkrapi20/demo/demo_sqlalchemy.bash

# This script should demo sqlalchemy

cd ~/tkrapi20/

. env.bash
export DATABASE_URL='postgres://tkrapi:tkrapi@127.0.0.1/tkrapi'

# Below, I list syntax I used to create role tkrapi and database tkrapi:
# sudo su - postgres
# psql
# CREATE ROLE tkrapi with login superuser password 'tkrapi';
# CREATE DATABASE tkrapi;

~/anaconda3/bin/python<<EOF
import os
import sqlalchemy as sql
# I should connect to the DB
db_s  = os.environ['DATABASE_URL']
conn  = sql.create_engine(db_s).connect()
sql_s = 'DROP TABLE IF EXISTS dropme'
conn.execute(sql_s)
sql_s = 'CREATE TABLE dropme(tkr varchar, crtime timestamp, cp float)'
conn.execute(sql_s)
# Notice how I use a python list to fill %s parameters:
sql_s = 'INSERT INTO dropme(tkr, crtime, cp)VALUES(%s, now(), %s)'
conn.execute(sql_s,['AAPL',99.01])
conn.execute(sql_s,['AMZN',100.01])
conn.execute(sql_s,['FB',100.02])
conn.execute(sql_s,['GOOG',100.03])
conn.execute(sql_s,['GOOG',100.10])
conn.execute(sql_s,['GOOG',100.11])
conn.execute(sql_s,['GOOG',100.12])
conn.execute(sql_s,['GOOG',100.13])
conn.execute(sql_s,['NFLX',100.04])
conn.execute(sql_s,['IBM',100.05])
sql_s  = 'SELECT * FROM dropme'
print(sql_s)
result = conn.execute(sql_s)
print(list(result))
# Notice how I use a python list to fill %s parameters:
sql_s  = 'SELECT * FROM dropme WHERE tkr = %s AND cp > %s'
print(sql_s)
result = conn.execute(sql_s,['GOOG',100.1])
print(list(result))
EOF

exit
