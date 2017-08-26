"""
dev.py

This script should help me do development.

Demo:
. env.bash
$PYTHON dev.py
"""

import codecs
import io
import pdb
import os
import flask
import datetime      as dt
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
import keras
# modules in the py folder:

import pgdb
import kerastkr
import sktkr


# I should connect to the DB
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()
sql_s = 'drop table if exists predictions'
conn.execute(sql_s)

tkr = 'FB'
yrs=3; mnth='2017-08'; features='pct_lag1,slope4,moy'
algo        = 'sklinear'

sktkr.learn_predict_sklinear(tkr, yrs, mnth, features)
# I should have a predictions table now

algo        = 'keraslinear'
algo_params = 'None Needed'
tkr = 'MSFT'

out_df = pgdb.dbpredictions(algo, tkr, yrs, mnth, features, algo_params)
print('This should be empty:')
print(out_df)

print('I should see loss output:')
out_df = pgdb.trydb_thenml(algo, tkr, yrs, mnth, features, algo_params)
print(out_df)

print('s.b. faster...:')
out_df = pgdb.trydb_thenml(algo, tkr, yrs, mnth, features, algo_params)
print(out_df)
stophere

algo        = 'kerasnn'
algo_params = '[3, 5]' # s.b. 1 space after comma!
tkr = 'IBM'

out_df = pgdb.dbpredictions(algo, tkr, yrs, mnth, features, algo_params)
print('This should be empty:')
print(out_df)

print('I should see loss output:')
out_df = pgdb.trydb_thenml(algo, tkr, yrs, mnth, features, algo_params)
print(out_df)

print('s.b. faster...:')
out_df = pgdb.trydb_thenml(algo, tkr, yrs, mnth, features, algo_params)
print(out_df)

out_df = pgdb.dbpredictions(algo, tkr, yrs, mnth, features, algo_params)
print('s.b. faster...:')
print(out_df)


'bye'
