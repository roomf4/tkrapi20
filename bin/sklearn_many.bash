#!/bin/bash

# sklearn_many.bash

# This script should learn-predict a tkr over several dimensions.

# The dimensions are:
# features:
# ["pct_lag1", "pct_lag2", "pct_lag4", "pct_lag8"
#  , "slope3", "slope4", "slope5", "slope6", "slope7", "slope8", "slope9"
#  , "dow", "moy"]
# yrs: [3,4,5,7,10,15,20,25,30]

# Demo:
# sklearn_many.bash IBM

if [ "$#" -ne 1 ]
then
    echo You should supply a Ticker.
    echo Demo:
    echo $0 IBM
    exit 1
fi

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

TKR=$1
YRS=3
FEATURES='["pct_lag1", "pct_lag2", "pct_lag8"]'

echo busy with:
echo \
$PYTHON py/sklearn_many.py $TKR $YRS $FEATURES
$PYTHON py/sklearn_many.py $TKR $YRS $FEATURES

# curl -v "lh:5013/csvtkr/sklinear/FB/3?features='pct_lag1,pct_lag2,pct_lag4'"
exit
