"""
flaskr.py

Demo:
. env.bash
$PYTHON flaskr.py
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
curl localhost:5011/sklinear/ABC/20/2016-12/'pct_lag1,slope3,dow,moy'
curl localhost:5011/keraslinear/ABC/20/2016-12/'pct_lag2,slope5,dow,moy'
curl "localhost:5011/kerasnn/IBM/25/2014-11?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
curl localhost:5011/sklinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
curl localhost:5011/sklinear_tkr/IBM/20/'pct_lag1,slope3,dow,moy'
curl localhost:5011/keraslinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
curl localhost:5011/kerasnn_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
curl localhost:5011/keraslinear_tkr/IBM/20/'pct_lag1,slope3,dow,moy'
curl "localhost:5011/db/kerasnn/IBM/3/2017-08?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
curl "localhost:5011/db1st_model2nd/kerasnn/WFC/4/2017-08?features='pct_lag1,slope3,moy'&hl=3&neurons=4"
curl "localhost:5011/dbyr/kerasnn/IBM/3/2017?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
curl "localhost:5011/dbtkr/kerasnn/IBM/3?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
curl "localhost:5011/db1st_model2nd_yr/kerasnn/WFC/4/2017?features='pct_lag1,slope3,moy'&hl=3&neurons=4"
curl "localhost:5011/db1st_model2nd_tkr/sklinear/WFC/4?features='pct_lag1,slope3,moy'&hl=3&neurons=4"
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
import sklearn.linear_model as skl
# modules in the py folder:
import pgdb
import sktkr
import kerastkr
import flaskclasses as flc

# I should connect to the DB
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()

# I should ready flask_restful:
application = fl.Flask(__name__)
api         = fr.Api(application)

# I should add classes and resources:

api.add_resource(flc.Demo11,    '/demo11.json')
api.add_resource(flc.AlgoDemos, '/algo_demos')
api.add_resource(flc.Demos,     '/demos')
api.add_resource(flc.Features,  '/features')
api.add_resource(flc.Tkrinfo,   '/tkrinfo/<tkr>')
api.add_resource(flc.Tkrlist,   '/tkrlist')
api.add_resource(flc.Tkrs,      '/tkrs')
api.add_resource(flc.DbTkrs,    '/dbtkrs')
api.add_resource(flc.Istkr,     '/istkr/<tkr>')
api.add_resource(flc.Tkrprices, '/tkrprices/<tkr>')
api.add_resource(flc.Sklinear,    '/sklinear/<tkr>/<int:yrs>/<mnth>/<features>')
api.add_resource(flc.SklinearYr,  '/sklinear_yr/<tkr>/<int:yrs>/<int:yr>/<features>')
api.add_resource(flc.SklinearTkr, '/sklinear_tkr/<tkr>/<int:yrs>/<features>')
api.add_resource(flc.KerasLinear,    '/keraslinear/<tkr>/<int:yrs>/<mnth>/<features>')
api.add_resource(flc.KeraslinearYr,  '/keraslinear_yr/<tkr>/<int:yrs>/<int:yr>/<features>')
api.add_resource(flc.KeraslinearTkr, '/keraslinear_tkr/<tkr>/<int:yrs>/<features>')
api.add_resource(flc.KerasNN,    '/kerasnn/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.KerasNNYr,  '/kerasnn_yr/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.KerasNNTkr, '/kerasnn_tkr/<tkr>/<int:yrs>')
api.add_resource(flc.Db,    '/db/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.Dbyr,  '/dbyr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.Dbtkr, '/dbtkr/<algo>/<tkr>/<int:yrs>')
api.add_resource(flc.Db1st,    '/db1st_model2nd/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.Db1stYr,  '/db1st_model2nd_yr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.Db1stTkr, '/db1st_model2nd_tkr/<algo>/<tkr>/<int:yrs>')
api.add_resource(flc.PredictionCounts, '/prediction_counts')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  application.run(host='0.0.0.0', port=port)
'bye'
