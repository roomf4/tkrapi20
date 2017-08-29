"""
flaskclasses.py

This script holds reusable flask classes.

"""

import io
import json
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
  
with open('tkrlist.txt') as fh:
  tkrlist_l = fh.read().split()

def get_out_d(out_df):
  """This function should convert out_df to a dictionary."""
  lo_acc  = sum((1+np.sign(out_df.pct_lead))/2) / out_df.accuracy.size
  # ref:
  # pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
  pd_json = out_df.to_json(orient='records')
  pd_d    = json.loads(pd_json)
  out_d   = {'Prediction-Details':pd_d
    ,'Long-Only-Accuracy'    :np.round(lo_acc, 3)
    ,'Long-Only-Effectivness':np.round(sum(out_df.pct_lead), 3)
    ,'Model-Effectivness'    :np.round(sum(out_df.effectiveness), 3)
    ,'Model-Accuracy'        :np.round(sum(out_df.accuracy) / out_df.accuracy.size, 3)
    ,'Prediction-Count'      :out_df.prediction.size
  }
  return out_d

class Demo11(fr.Resource):
  """
  This class should be a simple syntax demo.
  """
  def get(self):
    my_k_s = 'hello'
    my_v_s = 'world'
    return {my_k_s: my_v_s}

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
      ,"/kerasnn/FB/3/2017-07?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
      ,"/kerasnn_yr/FB/3/2017?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
      ,"/kerasnn_tkr/FB/3?features='pct_lag1,slope4,moy'&hl=2&neurons=4"
    ]
    return {
      'algo_demos': algo_demos_l
      ,'features':  pgdb.getfeatures()
    }

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

class Features(fr.Resource):
  """
  This class should return a list of available ML features.
  """
  def get(self):
    return {'features': pgdb.getfeatures()}

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

class Tkrlist(fr.Resource):
  """
  This class should list all the tkrs in tkrlist.txt
  """
  def get(self):
    return {'tkrlist': tkrlist_l, 'tkrcount': len(tkrlist_l)}

class Tkrs(fr.Resource):
  """
  This class should list all the tkrs in tkrlist.txt
  """
  def get(self):
    return {'tkrs': tkrlist_l, 'tkrcount': len(tkrlist_l)}

class DbTkrs(fr.Resource):
  """
  This class should list all the tkrs in tkrprices.
  """
  def get(self):
    dbtkrs_l = pgdb.dbtkrs()
    return {'tkrs': dbtkrs_l, 'tkrcount': len(dbtkrs_l)}

class Istkr(fr.Resource):
  """
  This class should answer True, False given a tkr.
  """
  def get(self, tkr):
    torf = tkr in tkrlist_l
    return {'istkr': torf}

class Tkrprices(fr.Resource):
  """
  This class should list prices for a tkr.
  """
  def get(self, tkr):
    return {'tkrprices': pgdb.tkrprices(tkr)}

class Sklinear(fr.Resource):
  """
  This class should return predictions from sklearn.
  """
  def get(self, tkr,yrs,mnth,features):
    features_s = pgdb.check_features(features)
    out_df = sktkr.learn_predict_sklinear(tkr,yrs,mnth,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class SklinearYr(fr.Resource):
  """
  This class should return predictions from sklearn for a Year.
  """
  def get(self, tkr,yrs,yr,features):
    features_s = pgdb.check_features(features)
    out_df = sktkr.learn_predict_sklinear_yr(tkr,yrs,yr,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class SklinearTkr(fr.Resource):
  """
  This class should return all predictions from sklearn for a tkr.
  """
  def get(self, tkr,yrs,features):
    features_s = pgdb.check_features(features)
    out_df = sktkr.learn_predict_sklinear_tkr(tkr,yrs,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class KerasLinear(fr.Resource):
  """
  This class should return predictions from keras.
  """
  def get(self, tkr,yrs,mnth,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear(tkr,yrs,mnth,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class KeraslinearYr(fr.Resource):
  """
  This class should return predictions from keras for a Year.
  """
  def get(self, tkr,yrs,yr,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear_yr(tkr,yrs,yr,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class KeraslinearTkr(fr.Resource):
  """
  This class should return all predictions from keras for a tkr.
  """
  def get(self, tkr,yrs,features):
    features_s = pgdb.check_features(features)
    out_df = kerastkr.learn_predict_keraslinear_tkr(tkr,yrs,features_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

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


class Db1st(fr.Resource):
  """
  Return predictions from db, if none, predictions from model.
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
    if (out_df.size > 0):
      out_d = get_out_d(out_df)
    else:
      if (algo == 'kerasnn'):
        out_d = KerasNN().get(tkr,yrs,mnth) # features_s global to KerasNN()
      elif (algo == 'keraslinear'):
        out_d = KerasLinear().get(tkr,yrs,mnth,features_s)
    return {'predictions': out_d}

class Db1stYr(fr.Resource):
  """
  Return predictions from db, if none, predictions from model for a year.
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
    if (out_df.size > 0):
      out_d = get_out_d(out_df)
    else:
      if (algo == 'kerasnn'):
        out_d = KerasNNYr().get(tkr,yrs,yr) # features_s global to KerasNN()
      elif (algo == 'keraslinear'):
        out_d = KerasLinearYr().get(tkr,yrs,yr,features_s)
      else:
        out_d = SklinearYr().get(tkr,yrs,yr,features_s)
    return {'predictions': out_d}

class Db1stTkr(fr.Resource):
  """
  Return predictions from db, if none, predictions from model for a year.
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
    if (out_df.size > 0):
      out_d = get_out_d(out_df)
    else:
      if (algo == 'kerasnn'):
        out_d = KerasNNTkr().get(tkr,yrs) # features_s global to KerasNN()
      elif (algo == 'keraslinear'):
        out_d = KerasLinearTkr().get(tkr,yrs,features_s)
      else:
        out_d = SklinearTkr().get(tkr,yrs,features_s)
    return {'predictions': out_d}

class PredictionCounts(fr.Resource):
  """
  Return prediction counts from db.
  """
  def get(self):
    import json
    # I should get prediction counts from pgdb.
    pc_df      = pgdb.prediction_counts()
    pc_df_json = pc_df.to_json(orient='index')
    # flask_restful wants to serve a Dictionary:
    pc_d       = json.loads(pc_df_json)
    return pc_d
'bye'
