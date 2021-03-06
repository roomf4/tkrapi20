"""
notf.py

This script should provide sytnax to connect flask-restful to a postgres db.
Also it should control downstream imports to avoid tensorflow.
"""

import io
import itertools
import json
import os
import pdb
import re
import flask         as fl
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql

with open('tkrlist.txt') as fh:
  tkrlist_l = fh.read().split()

def list2combos(lst):
  """This function should return all combinations of a list and its sublists."""
  combosn_l = [] # Nested combinations of lst
  for idx in range(len(lst)):
    combosn_l.append([mm for mm in itertools.combinations(lst,idx+1)])
  # I should remove some of the nesting:
  combos_l = []
  for mm_l in combosn_l:
    for mm in mm_l:
      combos_l.append(mm)
  return combos_l

  
def get_out_d(out_df):
  """This function should convert out_df to a dictionary."""
  if (out_df.empty):
    return {'no': 'predictions for this tkr, month, features (yet).'}
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

# I should connect to the DB
db_s = os.environ['DATABASE_URL']
conn = sql.create_engine(db_s).connect()

def delete_predictions():
  """This function should delete all rows from predictions table."""
  sql_s  = "delete from predictions"
  conn.execute(sql_s)
  return True

def featuresCSV(tkr):
  """This function should return CSV of features for a tkr."""
  tkru_s = tkr.upper()
  sql_s  = "select csv from features where tkr = %s  LIMIT 1"
  result = conn.execute(sql_s,[tkru_s])
  if not result.rowcount:
    return None
  return [row for row in result][0].csv

def getfeat(tkr):
  """This function should return a DataFrame full of features for a tkr."""
  csv_s = featuresCSV(tkr)
  if csv_s == None:
    return pd.DataFrame() # empty DF offers consistent behavior to caller.
  feat_df = pd.read_csv(io.StringIO(csv_s))
  return feat_df

def tkrpricesCSV(tkr):
  """This function should return CSV prices for a tkr."""
  tkru_s = tkr.upper()
  sql_s  = "select csvh from tkrprices where tkr = %s  LIMIT 1"
  result = conn.execute(sql_s,[tkru_s])
  if not result.rowcount:
    return None
  return [row for row in result][0].csvh

def tkrprices(tkr):
  """This function should return prices for a tkr."""
  csv_s = tkrpricesCSV(tkr)
  if (csv_s == None):
    return {'no': 'data found'}
  return {tkr.upper(): csv_s.split()}
  
def dbtkrs():
  """This function should return a list of tickers from db."""
  sql_s    = 'select tkr from tkrprices order by tkr'
  result   = conn.execute(sql_s)
  dbtkrs_l = [row.tkr for row in result]
  return dbtkrs_l

def getfeatures():
  """This function should return a list of valid features."""
  # I should get list from data rather than a software-constant.
  # This feels more DRY if I add features in the future:
  sql_s  = "SELECT csv FROM features WHERE tkr = 'FB' LIMIT 1"
  result = conn.execute(sql_s)
  if not result.rowcount:
    return ['no features found'] # Probably, a problem.
  myrow     = [row for row in result][0]
  feat_df   = pd.read_csv(io.StringIO(myrow.csv))
  columns_l = feat_df.columns.tolist()
  # I should remove cdate, cp, pct_lead:
  return columns_l[3:]

def check_features(f_s):
  """This function should check validity of f_s user input."""
  valid_features_l = getfeatures()
  features_s       = f_s.replace("'","").replace('"','')
  features_st      = set(features_s.split(','))
  goodfeatures_st  = set(valid_features_l).intersection(features_st)
  goodfeatures_s   = ','.join(sorted(goodfeatures_st))
  return goodfeatures_s

def tkrinfo(tkr):
  """This function should return info about a tkr."""
  feat_df             = getfeat(tkr)
  if feat_df.empty:
    return {'tkr': ('No info for: '+tkr)}
  observation_count_i = int(feat_df.cdate.size)
  maxdate_row = feat_df.loc[feat_df.cdate == feat_df.cdate.max()]
  return {
    'tkr':                 tkr
    ,'observation_count':  observation_count_i
    ,'years_observations': np.round(observation_count_i/252.0,1)
    ,'mindate':            feat_df.cdate.min()
    ,'maxdate':            feat_df.cdate.max()
    ,'maxdate_price':      maxdate_row.cp.tolist()[0]
  }

def get_train_test(tkr,yrs,mnth,features):
  """Using tkr,yrs,mnth,features, this function should get train,test numpy arrays."""
  xtrain_a = np.array(())
  ytrain_a = np.array(())
  xtest_a  = np.array(())
  out_df   = pd.DataFrame()
  feat_df  = getfeat(tkr)
  if (feat_df.empty):
    # I should return empty objects:
    return xtrain_a, ytrain_a, xtest_a, out_df
  # I should get the test data from feat_df:
  test_bool_sr = (feat_df.cdate.str[:7] == mnth)
  test_df      =  feat_df.loc[test_bool_sr] # should be about 21 rows
  if (test_df.empty):
    # I should return empty objects:
    return xtrain_a, ytrain_a, xtest_a, out_df
  # I should get the training data from feat_df:
  max_train_loc_i = -1 + test_df.index[0]
  min_train_loc_i = max_train_loc_i - yrs * 252
  if (min_train_loc_i < 10):
    # I should return empty objects:
    return xtrain_a, ytrain_a, xtest_a, out_df
  train_df = feat_df.loc[min_train_loc_i:max_train_loc_i]
  # I should train:
  features_l = features.split(',')
  xtrain_df  = train_df[features_l]
  xtrain_a   = np.array(xtrain_df)
  ytrain_a   = np.array(train_df)[:,2 ]
  xtest_df   = test_df[features_l]
  xtest_a    = np.array(xtest_df)
  out_df     = test_df.copy()[['cdate','cp','pct_lead']]
  return xtrain_a, ytrain_a, xtest_a, out_df

def getmonths4tkr(tkr,yrs):
  """Should return a List of mnth-strings suitable for learning from yrs years."""
  # I should get feat_df for tkr:
  feat_df = getfeat(tkr)
  if (feat_df.empty):
    # I should return empty List:
    return []
  # I should get a series of month-strings from feat_df.cdate
  mnth_sr = feat_df.cdate.str[:7] # Like: 2010-07
  mnth_a  = mnth_sr.unique() # Actually just unique values.
  mnth_l  = sorted(mnth_a.tolist())
  start_i     = 2+yrs*12 # I should start learning 2 months after yrs years.
  shortmnth_l = mnth_l[start_i:] # Should have enough history for learning.
  return shortmnth_l

def dbpredictions(algo  = 'sklinear'
           ,tkr         = 'FB'
           ,yrs         = 3 # years to train
           ,mnth        = '2017-08'
           ,features    = 'pct_lag1,slope4,moy'
           ,algo_params = 'None Needed'
           ):
  """This function should return saved predictions."""
  features_s = check_features(features)
  sql_s  = '''SELECT tkr, csv
    FROM predictions
    WHERE tkr         = %s
    AND   yrs         = %s
    AND   mnth        = %s
    AND   features    = %s
    AND   algo        = %s
    AND   algo_params = %s
    '''
  if (algo != 'kerasnn'):
    algo_params = 'None Needed'
  result = conn.execute(sql_s,[tkr,yrs,mnth,features_s,algo,algo_params])
  if not result.rowcount:
    return pd.DataFrame() # Maybe no predictions in db now.
  myrow  = [row for row in result][0]
  out_df = pd.read_csv(io.StringIO(myrow.csv))
  return out_df

def dbpredictions_yr(algo  = 'sklinear'
           ,tkr         = 'FB'
           ,yrs         = 3 # years to train
           ,yr          = '2017'
           ,features    = 'pct_lag1,slope4,moy'
           ,algo_params = 'None Needed'
           ):
  """This function should return saved predictions."""
  features_s = check_features(features)
  sql_s  = '''SELECT tkr, csv
    FROM predictions
    WHERE tkr         = %s
    AND   yrs         = %s
    AND   mnth like     %s
    AND   features    = %s
    AND   algo        = %s
    AND   algo_params = %s
    '''
  empty_df = pd.DataFrame()
  yr_l     = [empty_df, empty_df] # Ready for pd.concat()
  if (algo != 'kerasnn'):
    algo_params = 'None Needed'
  yrpat_s = str(yr)+'%' # s.b. like '2017%'
  result  = conn.execute(sql_s,[tkr,yrs,yrpat_s,features_s,algo,algo_params])
  if not result.rowcount:
    return pd.DataFrame() # Maybe no predictions in db now.
  # I should loop through result to collect a DataFrame for each month:
  for row in result:
    out_df = pd.read_csv(io.StringIO(row.csv))
    yr_l.append(out_df)
  yr_df = pd.concat(yr_l, ignore_index=True)
  return yr_df

def dbpredictions_tkr(algo  = 'sklinear'
           ,tkr         = 'FB'
           ,yrs         = 3 # years to train
           ,features    = 'pct_lag1,slope4,moy'
           ,algo_params = 'None Needed'
           ):
  """This function should return saved predictions."""
  features_s = check_features(features)
  sql_s  = '''SELECT tkr, csv
    FROM predictions
    WHERE tkr         = %s
    AND   yrs         = %s
    AND   features    = %s
    AND   algo        = %s
    AND   algo_params = %s
    '''
  empty_df = pd.DataFrame()
  yr_l     = [empty_df, empty_df] # Ready for pd.concat()
  if (algo != 'kerasnn'):
    algo_params = 'None Needed'
  result  = conn.execute(sql_s,[tkr,yrs,features_s,algo,algo_params])
  if not result.rowcount:
    return pd.DataFrame() # Maybe no predictions in db now.
  # I should loop through result to collect a DataFrame for each month:
  for row in result:
    out_df = pd.read_csv(io.StringIO(row.csv))
    yr_l.append(out_df)
  yr_df = pd.concat(yr_l, ignore_index=True)
  return yr_df

def prediction_counts():
  """This function should return aggregated prediction counts."""
  sql_s = '''
    select
    algo
    ,tkr
    ,yrs                   training_yrs
    ,features              feature_group
    ,substring(mnth for 4) yr
    ,count(tkr)            groups_of_predictions
    from predictions
    group by algo,tkr,yrs,features,substring(mnth for 4)
    order by algo,tkr,yrs,features,substring(mnth for 4)
    '''
  return pd.read_sql(sql_s, conn)

def prediction_dimensions():
  """This function should return prediction dimensions."""
  sql_s  = 'select distinct tkr from predictions'
  tkr_d  = json.loads(pd.read_sql(sql_s, conn).to_json())
  sql_s  = 'select distinct algo from predictions'
  algo_d = json.loads(pd.read_sql(sql_s, conn).to_json())
  sql_s  = 'select distinct yrs from predictions'
  yrs_d  = json.loads(pd.read_sql(sql_s, conn).to_json())
  sql_s  = 'select distinct substring(mnth for 4) yr from predictions'
  yr_d   = json.loads(pd.read_sql(sql_s, conn).to_json())
  sql_s  = 'select distinct features from predictions'
  features_d = json.loads(pd.read_sql(sql_s, conn).to_json())
  # I should merge dictionaries into 1:
  tkr_d.update(algo_d)
  tkr_d.update(yrs_d)
  tkr_d.update(yr_d)
  tkr_d.update(features_d)
  return tkr_d

def kerasnn_dimensions():
  """This function should return prediction dimensions."""
  sql_s  = "select distinct algo_params from predictions where algo = 'kerasnn'"
  algo_params_d = json.loads(pd.read_sql(sql_s, conn).to_json())
  return algo_params_d


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
      ,'features':  getfeatures()
    }

class Demos(fr.Resource):
  """
  This class should return a list of Demos.
  """
  def get(self):
    demos_l = [
      "/demos"
      ,"/demo11.json"
      ,"/features"
      ,"/prediction_counts"
      ,"/prediction_dimensions"
      ,"/kerasnn_dimensions"
      ,"/tkrs"
      ,"/tkrlist"
      ,"/tkrinfo/IBM"
      ,"/tkrprices/SNAP"
      ,"/istkr/YHOO"
      ,{'csv_demos':
        ["/csv/kerasnn/IBM/3/2017-08?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
        ,"/csvtkr/sklinear/FB/3features='pct_lag1,slope4,moy'"]}
      ,{'database_demos':
        ["/db/kerasnn/IBM/3/2017-08?features='pct_lag1,slope4,moy'&hl=3&neurons=5"
        ,"/dbtkr/sklinear/FB/3features='pct_lag1,slope4,moy'"]}
    ]
    return {'demos': demos_l}

class Features(fr.Resource):
  """
  This class should return a list of available ML features.
  """
  def get(self):
    return {'features': getfeatures()}

class Tkrinfo(fr.Resource):
  """
  This class should return info about a tkr.
  """
  def get(self, tkr):
    tkrinfo_d = None
    torf      = tkr in tkrlist_l
    if torf:
      tkrinfo_d = tkrinfo(tkr)
    return {'istkr': torf,'tkrinfo': tkrinfo_d}

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
    dbtkrs_l = dbtkrs()
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
    return {'tkrprices': tkrprices(tkr)}

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
    out_df = dbpredictions(algo,tkr,yrs,mnth,features_s,algo_params_s)
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
    out_df = dbpredictions_yr(algo,tkr,yrs,yr,features_s,algo_params_s)
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
    out_df = dbpredictions_tkr(algo,tkr,yrs,features_s,algo_params_s)
    out_d  = get_out_d(out_df)
    return {'predictions': out_d}

class PredictionCounts(fr.Resource):
  """
  Return prediction counts from db.
  """
  def get(self):
    # I should get prediction counts from db.
    pc_df      = prediction_counts()
    pc_df_json = pc_df.to_json(orient='index')
    # flask_restful wants to serve a Dictionary:
    pc_d       = json.loads(pc_df_json)
    return pc_d

class PredictionDimensions(fr.Resource):
  """
  Return prediction dimensions from db.
  """
  def get(self):
    pdim_d = prediction_dimensions()
    return pdim_d

class KerasnnDimensions(fr.Resource):
  """
  Return kerasnn algo_params dimensions from db.
  """
  def get(self):
    algo_params_d = kerasnn_dimensions()
    return algo_params_d
'bye'

