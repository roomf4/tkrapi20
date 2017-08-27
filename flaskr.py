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

api.add_resource(flc.Demo11,   '/demo11.json')
api.add_resource(flc.Db1st,    '/db1st_model2nd/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(flc.Db1stYr,  '/db1st_model2nd_yr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(flc.Db1stTkr, '/db1st_model2nd_tkr/<algo>/<tkr>/<int:yrs>')

class Db(fr.Resource):
  """
  This class should return predictions from db.
  """
  def get(self,algo,tkr,yrs,mnth):
    features0_s = fl.request.args.get('features', 'pct_lag1,slope4,dow')
    features_s    = features0_s.replace("'","").replace('"','')
    hl_s          = fl.request.args.get('hl',      '2') # default 2
    neurons_s     = fl.request.args.get('neurons', '4') # default 4
    hl_i          = int(hl_s)
    neurons_i     = int(neurons_s)
    algo_params_s = str([hl_i, neurons_i])
    # I should get predictions from db:
    out_df = pgdb.dbpredictions(algo,tkr,yrs,mnth,features_s,algo_params_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(Db, '/db/<algo>/<tkr>/<int:yrs>/<mnth>')

class Dbyr(fr.Resource):
  """
  This class should return predictions from db for a year.
  """
  def get(self,algo,tkr,yrs,yr):
    features0_s = fl.request.args.get('features','pct_lag1,slope4,dow')
    features_s    = features0_s.replace("'","").replace('"','')
    hl_s          = fl.request.args.get('hl',      '2') # default 2
    neurons_s     = fl.request.args.get('neurons', '4') # default 4
    hl_i          = int(hl_s)
    neurons_i     = int(neurons_s)
    algo_params_s = str([hl_i, neurons_i])
    # I should get predictions from db:
    out_df = pgdb.dbpredictions_yr(algo,tkr,yrs,yr,features_s,algo_params_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(Dbyr, '/dbyr/<algo>/<tkr>/<int:yrs>/<int:yr>')

class Dbtkr(fr.Resource):
  """
  This class should return predictions from db for a year.
  """
  def get(self,algo,tkr,yrs):
    features0_s = fl.request.args.get('features','pct_lag1,slope4,dow')
    features_s    = features0_s.replace("'","").replace('"','')
    hl_s          = fl.request.args.get('hl',      '2') # default 2
    neurons_s     = fl.request.args.get('neurons', '4') # default 4
    hl_i          = int(hl_s)
    neurons_i     = int(neurons_s)
    algo_params_s = str([hl_i, neurons_i])
    # I should get predictions from db:
    out_df = pgdb.dbpredictions_tkr(algo,tkr,yrs,features_s,algo_params_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
api.add_resource(Dbtkr, '/dbtkr/<algo>/<tkr>/<int:yrs>')

class AlgoDemos(fr.Resource):
  """
  This class should return a list of Algo Demos.
  """
  def get(self):
    algo_demos_l = [
      "/sklinear/IBM/20/2017-08/'pct_lag1,slope3,dow,moy'"
      ,"/sklinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'"
      ,"/sklinear_tkr/IBM/20/'pct_lag1,slope3,dow,moy'"
      ,"/keraslinear/FB/3/2017-08/'pct_lag2,slope5,moy'"
      ,"/keraslinear_yr/IBM/20/2016/'pct_lag1,slope3,dow,moy'"
      ,"/keraslinear_tkr/IBM/20/'pct_lag1,slope3,dow,moy'"
      ,"/keras_nn/FB/3/2017-07?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
      ,"/keras_nn_yr/FB/3/2017?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
      ,"/keras_nn_tkr/FB/3?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
    ]
    return {
      'algo_demos': algo_demos_l
      ,'features':  pgdb.getfeatures()
    }
api.add_resource(AlgoDemos, '/algo_demos')

class Demos(fr.Resource):
  """
  This class should return a list of Demos.
  """
  def get(self):
    demos_l = [
      "/demos"
      ,"/algo_demos"
      ,"/features"
      ,"/tkrs"
      ,"/tkrlist"
      ,"/years"
      ,"/tkrinfo/IBM"
      ,"/tkrprices/SNAP"
      ,"/istkr/YHOO"
      ,"/demo11.json"
      ,"/static/hello.json"
      ,AlgoDemos().get()
      ,{'database_demos':
        ["/db/kerasnn/IBM/3/2017-08?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
        ,"/db1st_model2nd/kerasnn/WFC/4/2017-08?features='pct_lag1,slope3,moy'&hl=3&neurons=4"]}
    ]
    return {'demos': demos_l}
api.add_resource(Demos, '/demos')

class Features(fr.Resource):
  """
  This class should return a list of available ML features.
  """
  def get(self):
    return {'features': pgdb.getfeatures()}
api.add_resource(Features, '/features')

class Tkrinfo(fr.Resource):
  """
  This class should return info about a tkr.
  """
  def get(self, tkr):
    tkrinfo   = None
    torf      = tkr in tkrlist_l
    if torf:
      tkrinfo = pgdb.tkrinfo(tkr)
    return {'istkr': torf,'tkrinfo': tkrinfo}
api.add_resource(Tkrinfo, '/tkrinfo/<tkr>')

class Tkrlist(fr.Resource):
  """
  This class should list all the tkrs in tkrlist.txt
  """
  def get(self):
    return {'tkrlist': tkrlist_l}
api.add_resource(Tkrlist, '/tkrlist')

class Tkrs(fr.Resource):
  """
  This class should list all the tkrs in tkrlist.txt
  """
  def get(self):
    return {'tkrs': tkrlist_l}
api.add_resource(Tkrs, '/tkrs')

class Istkr(fr.Resource):
  """
  This class should answer True, False given a tkr.
  """
  def get(self, tkr):
    torf = tkr in tkrlist_l
    return {'istkr': torf}
api.add_resource(Istkr, '/istkr/<tkr>')

class Years(fr.Resource):
  """
  This class should list all the years in years.txt
  """
  def get(self):
    return {'years': years_l}
api.add_resource(Years, '/years')

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
api.add_resource(Tkrprices, '/tkrprices/<tkr>')
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
api.add_resource(KerasLinear, '/keraslinear/<tkr>/<int:yrs>/<mnth>/<features>')
  
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
api.add_resource(KerasNN, '/keras_nn/<tkr>/<int:yrs>/<mnth>')

class SklinearYr(fr.Resource):
  """
  This class should return predictions from sklearn for a Year.
  """
  def get(self, tkr,yrs,yr,features):
    features_s = pgdb.check_features(features)
    out_df = sktkr.learn_predict_sklinear_yr(tkr,yrs,yr,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}
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
api.add_resource(KeraslinearYr, '/keraslinear_yr/<tkr>/<int:yrs>/<int:yr>/<features>')

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
api.add_resource(KerasNNYr, '/keras_nn_yr/<tkr>/<int:yrs>/<int:yr>')

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
api.add_resource(KeraslinearTkr, '/keraslinear_tkr/<tkr>/<int:yrs>/<features>')

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
api.add_resource(KerasNNTkr, '/keras_nn_tkr/<tkr>/<int:yrs>')
  
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  application.run(host='0.0.0.0', port=port)
'bye'
