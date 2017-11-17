#!/bin/bash

# ~/tkrapi20/demo/cr_model.bash

# This script should demo cr_model.py
# which depends on get_train_test() in pgdb.py
# to get training,testing data from a table called features.
# Once cr_model.py has the data it depends on sklearn.linear_model
# to fit a linear model to the training data.
# Then from that model it predicts observations in the test data and
# aligns them with real observations in out_df.
# This alignment allows me to see both accuracy and effectiveness of the model.

cd ~/tkrapi20/
. env.bash

~/anaconda3/bin/python <<EOF
import cr_model
tkr        = 'FB'
yrs        = 4
mnth       = '2017-10'
features_s = 'pct_lag1,pct_lag4,slope3,slope6,moy'
out_df = cr_model.cr_sklinear_model(tkr,yrs,mnth,features_s)
print(out_df)
EOF

# I should see a new, recent row in mlmodels:

bin/psql.bash <<EOF
SELECT * FROM mlmodels
WHERE tkr = 'FB'
AND yrs   = 4
AND mnth  = '2017-10'
AND algo  = 'sklinear'
ORDER BY crtime;
EOF

exit
