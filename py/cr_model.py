"""
cr_model.py

This script should create ML-models and save them to db table: mlmodels.

Demo:
. ../env.bash
$PYTHON cr_model.py
"""

import pdb
# modules in the py folder:
import kerastkr
import pgdb
import sktkr

def cr_sklinear_model(tkr='^GSPC', yrs=20, mnth='2017-08', features='pct_lag1,slope3,moy'):
  """This function should use sklearn to create a model."""
  features_s = pgdb.check_features(features)
  return True

pdb.set_trace()
cr_sklinear_model()

'bye'
