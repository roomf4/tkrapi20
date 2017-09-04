"""
sklearn_many.py

This script should learn-predict a tkr given some parameters.

Demo:
. env.bash
$PYTHON py/sklearn_many.py FB 3 '["pct_lag1", "pct_lag2", "pct_lag4"]'
"""

import sktkr
#learn_predict_sklinear_tkr(tkr='ABC',yrs=20, features='pct_lag1,slope4,moy')
sktkr.learn_predict_sklinear_tkr(
    'FB'
    ,3
    ,features='"pct_lag1", "pct_lag2", "pct_lag4"'
)

'bye'

