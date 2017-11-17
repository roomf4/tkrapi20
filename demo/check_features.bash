#!/bin/bash

# check_features.bash

# This script should demo pgdb.check_features(features)

cd ~/tkrapi20/
. env.bash

~/anaconda3/bin/python <<EOF
import pgdb
features_s = 'pct_lag1,slope4,moy'
print(pgdb.check_features(features_s))
EOF

exit
