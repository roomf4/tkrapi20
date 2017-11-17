#!/bin/bash

# ~/tkrapi20/demo/cr_model.bash

# This script should demo cr_model.py

cd ~/tkrapi20/
. env.bash

~/anaconda3/bin/python <<EOF
import cr_model
tkr  = 'FB'
yrs  = 4
mnth = '2017-10'
features_s = 'pct_lag1,pct_lag4,slope3,slope6,moy'
cr_model.cr_sklinear_model(tkr,yrs,mnth,features_s)
EOF

exit
