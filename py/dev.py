"""
dev.py

This script should help me do development.

Demo:
. env.bash
$PYTHON dev.py
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
# from the py folder:
import notf
import sktkr
import kerastkr

pdb.set_trace()
sktkr.learn_predict_sklinear('FB',4,'2017-08','pct_lag1,slope4,moy')
kerastkr.learn_predict_keraslinear('FB',4,'2017-08','pct_lag1,slope4,moy')

stophere
print(notf.tkrprices('SNAP'))
print(notf.featuresCSV('SNAP')[:77])
print(notf.getfeat('SNAP').tail())
print(notf.tkrpricesCSV('SNAP')[:77])
print(notf.getfeatures())
print(notf.tkrinfo('SNAP'))
print(notf.getmonths4tkr('FB',3))
print(notf.dbpredictions_tkr())
print(notf.prediction_counts())
print(notf.prediction_dimensions())
print(notf.kerasnn_dimensions())

'bye'

