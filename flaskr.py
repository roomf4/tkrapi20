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
curl "localhost:5011/keras_nn/IBM/25/2014-11?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
curl localhost:5011/sklinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
curl localhost:5011/sklinear_tkr/IBM/20/'pct_lag1,slope3,dow,moy'
curl localhost:5011/keraslinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
curl localhost:5011/keras_nn_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'
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

# I should fill lists which users want frequently:
with open('years.txt') as fh:
  years_l = fh.read().split()
  
with open('tkrlist.txt') as fh:
  tkrlist_l = fh.read().split()

# I should add classes and resources:

api.add_resource(flc.Demo11,    '/demo11.json')
api.add_resource(flc.AlgoDemos, '/algo_demos')
api.add_resource(flc.Demos,     '/demos')
api.add_resource(flc.Features,  '/features')
api.add_resource(flc.Tkrinfo,   '/tkrinfo/<tkr>')
api.add_resource(flc.Tkrlist,   '/tkrlist')
api.add_resource(flc.Tkrs,      '/tkrs')
api.add_resource(flc.Istkr,     '/istkr/<tkr>')
api.add_resource(flc.Db,    '/db/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.Dbyr,  '/dbyr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.Dbtkr, '/dbtkr/<algo>/<tkr>/<int:yrs>')
api.add_resource(flc.Db1st,    '/db1st_model2nd/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.Db1stYr,  '/db1st_model2nd_yr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.Db1stTkr, '/db1st_model2nd_tkr/<algo>/<tkr>/<int:yrs>')


class Tkrprices(fr.Resource):
  """
  This class should list prices for a tkr.
  """
  def get(self, tkr):
    # I should get csvh from tkrprices in db:
    sql_s  = "select csvh from tkrprices where tkr = %s  LIMIT 1"
    result = conn.execute(sql_s,[tkr])
    if not result.rowcount:
      return {'no': 'data found'}  
    myrow  = [row for row in result][0]
    return {'tkrprices': myrow.csvh.split()}
api.add_resource(flc.Tkrprices, '/tkrprices/<tkr>')
api.add_resource(flc.Sklinear, '/sklinear/<tkr>/<int:yrs>/<mnth>/<features>')

class KerasLinear(fr.Resource):
  """
  This class should return predictions from keras.
  """
  def get(self, tkr,yrs,mnth,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear(tkr,yrs,mnth,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KerasLinear, '/keraslinear/<tkr>/<int:yrs>/<mnth>/<features>')
  
class KerasNN(fr.Resource):
  """
  This class should return predictions from keras.
  """
  def get(self, tkr,yrs,mnth):
    features0_s = fl.request.args.get('features', 'pct_lag1,slope3,dom')
    features_s = pgdb.check_features(features0_s)
    hl_s       = fl.request.args.get('hl', '2')      # default 2
    neurons_s  = fl.request.args.get('neurons', '4') # default 4
    hl_i       = int(hl_s)
    neurons_i  = int(neurons_s)
    out_df = kerastkr.learn_predict_kerasnn(tkr,yrs,mnth,features_s,hl_i,neurons_i)
    out_d      = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KerasNN, '/keras_nn/<tkr>/<int:yrs>/<mnth>')

api.add_resource(flc.SklinearYr, '/sklinear_yr/<tkr>/<int:yrs>/<int:yr>/<features>')

class KeraslinearYr(fr.Resource):
  """
  This class should return predictions from keras for a Year.
  """
  def get(self, tkr,yrs,yr,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear_yr(tkr,yrs,yr,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KeraslinearYr, '/keraslinear_yr/<tkr>/<int:yrs>/<int:yr>/<features>')

class KerasNNYr(fr.Resource):
  """
  This class should return predictions from keras for a Year.
  """
  def get(self, tkr,yrs,yr):
    features0_s = fl.request.args.get('features', 'pct_lag1,slope3,dow')
    features_s = pgdb.check_features(features0_s)
    hl_s       = fl.request.args.get('hl', '2')      # default 2
    neurons_s  = fl.request.args.get('neurons', '4') # default 4
    hl_i       = int(hl_s)
    neurons_i  = int(neurons_s)
    out_df = kerastkr.learn_predict_kerasnn_yr(tkr,yrs,yr,features_s,hl_i,neurons_i)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KerasNNYr, '/keras_nn_yr/<tkr>/<int:yrs>/<int:yr>')

api.add_resource(flc.SklinearTkr, '/sklinear_tkr/<tkr>/<int:yrs>/<features>')

class KeraslinearTkr(fr.Resource):
  """
  This class should return all predictions from keras for a tkr.
  """
  def get(self, tkr,yrs,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear_tkr(tkr,yrs,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KeraslinearTkr, '/keraslinear_tkr/<tkr>/<int:yrs>/<features>')

class KerasNNTkr(fr.Resource):
  """
  This class should return all predictions from keras for a tkr.
  """
  def get(self, tkr,yrs):
    features0_s = fl.request.args.get('features', 'pct_lag1,slope3,dow')
    features_s = pgdb.check_features(features0_s)
    hl_s       = fl.request.args.get('hl', '2')      # default 2
    neurons_s  = fl.request.args.get('neurons', '4') # default 4
    hl_i       = int(hl_s)
    neurons_i  = int(neurons_s)
    out_df = kerastkr.learn_predict_kerasnn_tkr(tkr,yrs,features_s,hl_i,neurons_i)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(flc.KerasNNTkr, '/keras_nn_tkr/<tkr>/<int:yrs>')
  
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  application.run(host='0.0.0.0', port=port)
'bye'
