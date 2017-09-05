"""
sklearn_many.py

This script should learn-predict a tkr given some parameters.

Demo:
. env.bash
$PYTHON py/sklearn_many.py FB 3 '["pct_lag1", "pct_lag2", "pct_lag4"]'
"""

import pdb
import sys
pdb.set_trace()

import sktkr

if (len(sys.argv) != 2):
  print('I see a problem. Maybe you forgot a tkr?')
  print('Demo:')
  print('~/anaconda3/bin/python '+sys.argv[0]+' IBM')
  #  sys.exit(1)
  
# I should get the tkr from the command line
tkr = sys.argv[1]
yrs_i = int(sys.argv[2])
features_s = sys.argv[3:]
#learn_predict_sklinear_tkr(tkr='ABC',yrs=20, features='pct_lag1,slope4,moy')
sktkr.learn_predict_sklinear_tkr(
    'FB'
    ,3
    ,features='"pct_lag1", "pct_lag2", "pct_lag4"'
)

'bye'

