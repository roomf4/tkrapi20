"""
sklearn_many.py

This script should learn-predict a tkr given some parameters.

Demo:
. env.bash
$PYTHON py/sklearn_many.py FB 3
"""

import datetime
import pdb
import sys

import notf
import sktkr

if (len(sys.argv) < 2):
  print('I see a problem. Maybe you forgot a tkr?')
  print('Demo:')
  print('~/anaconda3/bin/python '+sys.argv[0]+' IBM 3')
  #  sys.exit(1)
  
# I should get the tkr from the command line
tkr   =     sys.argv[1]
yrs_i = int(sys.argv[2])
lags_s   = ',pct_lag2,pct_lag8'
slopes_s = ',slope3,slope4' #,slope5,slope6,slope7,slope8,slope9'
datef_s  = ',dow,moy'
features_always_s    = 'pct_lag1,pct_lag4,'
features_sometimes_s = lags_s + slopes_s + datef_s

# I should get all combinations of features in features_sometimes_s.
features_l = sorted(features_sometimes_s.split(','))
features_l.remove('')
print(features_l)

combos_l = notf.list2combos(features_l)

# I should ask which month it is now:
mnth = datetime.datetime.now().strftime('%Y-%m')

# I should collect predictions for each combo:
for combo in combos_l:
  combo_s = ','.join(combo)
  features_s = features_always_s + combo_s
  print(features_s)
  'sktkr.learn_predict_sklinear(tkr,yrs_i,mnth,features_s)'
# I should not forget this one:
sktkr.learn_predict_sklinear(tkr,yrs_i,mnth,features_always_s)

'bye'

