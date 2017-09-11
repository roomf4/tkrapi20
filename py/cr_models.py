"""
cr_models.py

# This script should insert many models into mlmodels table.
"""

import cr_model
import pgdb

tkr = '^GSPC'
features_skinny_s = 'pct_lag1,slope3,moy'
features_medium_s = 'pct_lag1,pct_lag4,slope3,slope6,moy'
features_wide_s   = 'pct_lag1,pct_lag2,pct_lag4,pct_lag8,slope3,slope4,slope5,slope6,slope7,slope8,slope9,dow,moy'

for yrs in (10,20,30):
  for features_s in (features_skinny_s,features_medium_s,features_wide_s):
    print(tkr,yrs,features_s)
    for mnth in pgdb.getmonths4tkr(tkr,yrs):
      cr_model.cr_sklinear_model(tkr,yrs,mnth,features_s)


'bye'
