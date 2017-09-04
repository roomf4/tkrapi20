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

