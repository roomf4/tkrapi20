"""
cr_model.py

This script should create ML-models and save them to db table: mlmodels.
"""

import io
import pdb
import os
import datetime      as dt
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
import sklearn.linear_model as skl
# modules in the py folder:
import kerastkr
import pgdb
import sktkr

# I should connect to the DB
db_s = os.environ['DATABASE_URL']
conn = sql.create_engine(db_s).connect()

def model2db(tkr,yrs,mnth,features,algo,coef_s):
  """This function should save ML-model to db table: mlmodels."""
  # This function depends on: sql/cr_mlmodels.sql
  # Eventually I should replace DELETE/INSERT with UPSERT:
  sql_s = '''DELETE FROM mlmodels
    WHERE tkr         = %s
    AND   yrs         = %s
    AND   mnth        = %s
    AND   features    = %s
    AND   algo        = %s
    '''
  conn.execute(sql_s,[tkr,yrs,mnth,features,algo])
  # I should insert coef_s into mlmodels:
  sql_s = '''INSERT INTO mlmodels(
    tkr, yrs,mnth,features,algo,crtime,sklinear_coef)VALUES(
    %s , %s ,%s  ,%s      ,%s  ,now() ,%s)'''
  conn.execute(sql_s,[
    tkr, yrs,mnth,features,algo       ,coef_s])
  # check: select * from mlmodels order by crtime desc limit 3;
  return True

def cr_sklinear_model(tkr='^GSPC', yrs=20, mnth='2017-08', features='pct_lag1,slope3,moy'):
  """This function should use sklearn to create a model."""
  features_s = pgdb.check_features(features)
  linr_model = skl.LinearRegression()
  xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,yrs,mnth,features_s)
  if ((xtrain_a.size == 0) or (ytrain_a.size == 0) or (xtest_a.size == 0)):
    return out_df # probably empty too.
  # I should fit a model to xtrain_a, ytrain_a
  # I should get intercept and coefficients:
  linr_model.fit(xtrain_a,ytrain_a)
  # I should predict xtest_a then update out_df
  out_df['prediction']    = np.round(linr_model.predict(xtest_a),3).tolist()
  out_df['effectiveness'] = np.sign(out_df.pct_lead*out_df.prediction)*np.abs(out_df.pct_lead)
  out_df['accuracy']      = (1+np.sign(out_df.effectiveness))/2
  algo   = 'sklinear'
  kmodel = None # sklearn has no kmodel, keras does.
  # I should save work to the db:
  coef_f_l = [linr_model.intercept_] + linr_model.coef_.tolist()
  coef_l   = [str(mem_s) for mem_s in coef_f_l]
  coef_s   = ','.join(coef_l)
  # I should save tkr,yrs,mnth,features_s,algo,coef_s
  model2db(tkr,yrs,mnth,features_s,algo,coef_s)
  return out_df



'bye'
