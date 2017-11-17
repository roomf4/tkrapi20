#!/bin/bash

# ~/tkrapi20/demo/get_train_test.bash

# This script should demo how to call pgdb.get_train_test()
# which is a method I use to get data ready for training and testing.

cd ~/tkrapi20/
. env.bash

~/anaconda3/bin/python <<EOF
import pgdb
tkr        = 'FB'
yrs        = 4
mnth       = '2017-10'
features_s = 'pct_lag1,slope4,moy'
xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,yrs,mnth,features_s)
print(xtrain_a[:9])
print(ytrain_a[:9])
print(xtest_a)
print(out_df)
EOF

exit
