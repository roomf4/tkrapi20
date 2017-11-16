"""
pgdb.py

This script should provide sytnax to connect flask-restful to a postgres db.

"""

import io
import json
import os
import pdb
import re
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
# modules in the py folder:
import sktkr
import kerastkr
import notf

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

def getfeat2file(tkr):
  """This function should write a CSV-file full of features for a tkr."""
  feat_df = getfeat(tkr)
  csvf_s  = '/tmp/feat'+tkr+'.csv'
  feat_df.to_csv(csvf_s, index=False, float_format='%.3f')
  
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
  features_s       = (f_s.replace("'","").
                      replace('"','').
                      replace(' ','').
                      replace('[','').
                      replace(']',''))
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

def predictions2db(tkr,yrs,mnth,features,algo,predictions_df,kmodel,coef=None,algo_params='None Needed'):
  """This function should copy predictions and reporting columns to db."""
  # I should format features to make them consistent:
  features_s = pgdb.check_features(features)
  if coef:
    coef_s = str(coef)
  else:
    coef_s = None # s. become NULL in db.
  if kmodel: # If I am using keras.
    kmodel.save('/tmp/kmodel.h5')
    with open('/tmp/kmodel.h5','rb') as fh:
      kmodel_h5 = fh.read() # kmodel_h5 s.b. different than kmodel
  else: # I am not using keras.
    kmodel_h5   = None # db should convert this to NULL during INSERT.
  # I should convert DF to a string
  csv_s = predictions_df.to_csv(index=False,float_format='%.3f')
  # I should move CREATE TABLE to an initialization script.
  # Running this statement frequently is inefficient:
  sql_s = '''CREATE TABLE IF NOT EXISTS
    predictions(
    tkr          VARCHAR
    ,yrs         INTEGER
    ,mnth        VARCHAR
    ,features    VARCHAR
    ,algo        VARCHAR
    ,algo_params VARCHAR
    ,crtime      TIMESTAMP
    ,sklinear_coef TEXT
    ,csv           TEXT
    ,kmodel_h5     BYTEA
  )'''
  conn.execute(sql_s) # should be ok for now.
  # Eventually I should replace DELETE/INSERT with UPSERT:
  sql_s = '''DELETE FROM predictions
    WHERE tkr         = %s
    AND   yrs         = %s
    AND   mnth        = %s
    AND   features    = %s
    AND   algo        = %s
    AND   algo_params = %s
    '''
  conn.execute(sql_s,[tkr,yrs,mnth,features_s,algo,algo_params])
    # I should match %s tokens with each column:
  sql_s = '''INSERT INTO predictions(
    tkr, yrs,mnth,features,algo,algo_params,crtime,sklinear_coef,csv,kmodel_h5)VALUES(
    %s , %s ,%s  ,%s      ,%s  ,%s         ,now() ,%s           ,%s ,%s)'''
  conn.execute(sql_s,[
    tkr, yrs,mnth,features_s,algo,algo_params,       coef_s,csv_s,kmodel_h5])
  return True

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

def db1st_model2nd(algo   = 'sklinear'
           ,tkr         = 'FB'
           ,yrs         = 3 # years to train
           ,mnth        = '2017-08'
           ,features    = 'pct_lag1,slope4,moy'
           ,algo_params = 'None Needed'
           ):
  """Predictions from db first, if none, then ML."""
  out_df = dbpredictions(algo, tkr, yrs, mnth, features, algo_params)
  if (out_df.size > 0):
    return out_df
  else: # then ML:
    if (algo   == 'sklinear'):
      out_df = sktkr.learn_predict_sklinear(      tkr, yrs, mnth, features)
    elif (algo == 'keraslinear'):
      out_df = kerastkr.learn_predict_keraslinear(tkr, yrs, mnth, features)
    else: # algo    s.b. kerasnn
      # algo_params s.b a string like this: '[2,4]'
      # Which specifies 2 hidden layers with 4 neurons in each.
      pattern_re = r'(\[)(\d+)(, )(\d+)(\])'
      pattern_ma = re.search(pattern_re,algo_params)
      hl_i       = int(pattern_ma[2])
      neurons_i  = int(pattern_ma[4])
      out_df     = kerastkr.learn_predict_kerasnn(tkr
                                              ,yrs
                                              ,mnth
                                              ,features
                                              ,hl_i
                                              ,neurons_i)
    return out_df
  
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

'bye'
