"""
predictfrom_mlmodels.py

# This script should demo how to generate predictions from mlmodels table.

# Demo:

. env.bash

$PYTHON py/predictfrom_mlmodels.py
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
import cr_model
import pgdb

# I should connect to the DB
db_s = os.environ['DATABASE_URL']
conn = sql.create_engine(db_s).connect()

# I should use python to get a model from  mlmodels table.

# select * from mlmodels order by crtime desc limit 1;

sql_s  = "select * from mlmodels order by crtime desc limit 1"

result = conn.execute(sql_s)

for row in result:
  print(row.tkr)
  tkr  = row.tkr
  mnth = row.mnth
  features = row.features
  coef_s   = row.sklinear_coef
  
# I should use python to get suitable test data from features table,
# using tkr:

feat_df = pgdb.getfeat(tkr)
print(feat_df.tail())

# I should extract a numpy array from feat_df

print(tkr,5,mnth)
print(pgdb.check_features(features))
xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,5,mnth,pgdb.check_features(features))
print(out_df)
print(xtest_a)

# I should transform coef_s into array:
print(coef_s)
pdb.set_trace()
coef_l = coef_s.split(',')
coef_a = np.array(coef_l).reshape(len(coef_l),-1).astype(float)
print(coef_a)

# I should calc predictions using matmul:

# I should add a column of 1s to xtest_a
a1_a  = np.ones((len(xtest_a),1), dtype=np.float)
test_a = np.concatenate((a1_a,xtest_a), axis=1)# horizontally
predictions_a = np.matmul(test_a,coef_a)


'bye'

