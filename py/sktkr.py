"""
sktkr.py

This script should use sklearn to learn from stock market data.

Demo:
. env.bash
$PYTHON
import  sktkr
sktkr.learn_predict_sklinear('FB',4,'2017-08','pct_lag1,slope4,moy')
"""

import io
import pdb
import os
import flask
import datetime      as dt
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
import sklearn.linear_model as skl
# modules in the py folder:
import pgdb

# By default, I should train from 20 years of data.

def learn_predict_sklinear(tkr='ABC',yrs=20,mnth='2016-11', features='pct_lag1,slope4,moy'):
  """This function should use sklearn to learn, predict."""
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
  pgdb.predictions2db(tkr,yrs,mnth,features_s,algo,out_df,kmodel,coef_s)
  return out_df

def learn_predict_sklinear_yr(tkr='ABC',yrs=20,yr=2016, features='pct_lag1,slope4,moy'):
  """This function should use sklearn to learn and predict for a year."""
  empty_df = pd.DataFrame()
  yr_l     = [empty_df, empty_df] # Ready for pd.concat()
  # I should rely on monthy predictions:
  for mnth_i in range(1,13):
    mnth_s = str(mnth_i).zfill(2)
    mnth   = str(yr)+'-'+mnth_s
    m_df   = learn_predict_sklinear(tkr,yrs,mnth, features)
    yr_l.append(m_df)
  # I should gather the monthy predictions:
  yr_df = pd.concat(yr_l, ignore_index=True)
  return yr_df

def learn_predict_sklinear_tkr(tkr='ABC',yrs=20, features='pct_lag1,slope4,moy'):
  """This function should use sklearn to learn and predict for a tkr."""
  # From db, I should get a list of all months for tkr:
  mnth_l = pgdb.getmonths4tkr(tkr,yrs)
  # I should rely on monthy predictions:
  empty_df = pd.DataFrame()
  tkr_l    = [empty_df, empty_df] # Ready for pd.concat()
  for mnth_s in mnth_l:
    m_df = learn_predict_sklinear(tkr,yrs,mnth_s, features)
    tkr_l.append(m_df)
  # I should gather the monthy predictions:
  tkr_df = pd.concat(tkr_l, ignore_index=True)
  return tkr_df

'bye'
