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
import sktkr

# I should connect to the DB
db_s = os.environ['DATABASE_URL']
conn = sql.create_engine(db_s).connect()

features_skinny_s = 'pct_lag1,slope3,moy'
features_medium_s = 'pct_lag1,pct_lag4,slope3,slope6,moy'

# I should use older syntax to ensure I have a model for this script:
tkr  = '^GSPC'
yrs  = 25
mnth = '2017-08'
features_s = features_medium_s
cr_model.cr_sklinear_model(tkr,yrs,mnth,features_s)

# I should use python to get a model from  mlmodels table.

# select * from mlmodels order by crtime desc limit 1;
sql_s  = '''select
tkr,yrs,mnth,features,sklinear_coef
from mlmodels order by crtime desc limit 1
'''

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

xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,5,mnth,pgdb.check_features(features))

# I should transform coef_s into array:
coef_l = coef_s.split(',')
coef_a = np.array(coef_l).reshape(len(coef_l),-1).astype(float)

# I should calc predictions using matmul:

# I should add a column of 1s to xtest_a
a1_a   = np.ones((len(xtest_a),1), dtype=np.float)
test_a = np.concatenate((a1_a,xtest_a), axis=1)# horizontally
predictions_a = np.matmul(test_a,coef_a)
print('predictions_a from matmul:')
print(predictions_a)

# I should use sklearn too:

out_df = sktkr.learn_predict_sklinear(tkr,yrs,mnth,features)
pdb.set_trace()
print(out_df.prediction)

'bye'

