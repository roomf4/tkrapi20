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
'bye'
