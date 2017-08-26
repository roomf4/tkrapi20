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

tkr='FB'; yrs=3; mnth='2017-08'; features='pct_lag1,slope4,moy'
out_df = sktkr.learn_predict_sklinear(tkr, yrs, mnth, features)
print(out_df)

algo        = 'sklinear'
algo_params = 'None Needed'

out_df = pgdb.dbalgo(tkr, yrs, mnth, features, algo, algo_params)
print(out_df)

'bye'
