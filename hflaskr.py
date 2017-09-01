"""
hflaskr.py

Demo:
. env.bash
$PYTHON hflaskr.py
Other shell:
curl localhost:5011/demo11.json
curl localhost:5011/static/hello.json
curl localhost:5011/demos
curl localhost:5011/features
curl localhost:5011/algo_demos
curl localhost:5011/tkrs
curl localhost:5011/tkrlist
curl localhost:5011/istkr/IBM
curl localhost:5011/tkrinfo/IBM
curl localhost:5011/years
curl localhost:5011/tkrprices/SNAP
curl "localhost:5011/db/kerasnn/IBM/3/2017-08?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
curl "localhost:5011/dbyr/kerasnn/IBM/3/2017?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
curl "localhost:5011/dbtkr/kerasnn/IBM/3?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
"""

import io
import pdb
import os
import datetime      as dt
import flask         as fl
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
# modules in the py folder:
import pgdb
import flaskclasses as flc

# I should connect to the DB
db_s = os.environ['PGURL']

if 'LOCALDB' in os.environ:
    # I should set LOCALDB on my laptop.
    'I should use PGURL'
else:
    # Heroku shell should not see LOCALDB
    db_s = os.environ['HPGURL']

stophere

conn = sql.create_engine(db_s).connect()

# I should ready flask_restful:
application = fl.Flask(__name__)
api         = fr.Api(application)

# I should add resources:

api.add_resource(flc.Demo11, '/demo11.json')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5012))
  application.run(host='0.0.0.0', port=port)
'bye'

