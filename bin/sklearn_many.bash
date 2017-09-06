#!/bin/bash

# sklearn_many.bash

# This script should learn-predict over several dimensions.

# The dimensions are:
# features:
# ["pct_lag1", "pct_lag2", "pct_lag4", "pct_lag8"
#  , "slope3", "slope4", "slope5", "slope6", "slope7", "slope8", "slope9"
#  , "dow", "moy"]
# yrs: [3,4,5,7,10,15,20,25,30]
# tkrs: ['AAPL','FB',IBM','^GSPC', ... (about 725)]

# Demo:
# bin/sklearn_many.bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

# for TKR in AAPL FB IBM ^GSPC
head -5 ${PARPATH}/tkrlist_small.txt| while read TKR
do
  for YRS in 3 4 # 5 7 10 15 20 15 30
  do
    echo busy with:
    echo \
    $PYTHON py/sklearn_many.py $TKR $YRS
    $PYTHON py/sklearn_many.py $TKR $YRS
  done
done

exit
# I should see if we have new predictions now:
# curl -v "lh:5013/csvtkr/sklinear/FB/3?features='pct_lag1,pct_lag2,pct_lag4'"
exit
