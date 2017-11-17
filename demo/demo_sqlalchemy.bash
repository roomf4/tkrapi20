#!/bin/bash

# ~/tkrapi20/demo/demo_sqlalchemy.bash

# This script should demo sqlalchemy

cd ~/tkrapi20/

. env.bash
export DATABASE_URL='postgres://tkrapi:tkrapi@127.0.0.1/tkrapi'

~/anaconda3/bin/python<<EOF
import os
import sqlalchemy as sql
# I should connect to the DB
db_s  = os.environ['DATABASE_URL']
conn  = sql.create_engine(db_s).connect()
sql_s = 'SELECT COUNT(tkr) count_tkr,tkr,algo FROM mlmodels GROUP BY tkr,algo'
result = conn.execute(sql_s)
print([row for row in result])
EOF

exit
