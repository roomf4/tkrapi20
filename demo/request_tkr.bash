#!/bin/bash

# ~/tkrapi20/demo/request_tkr.bash

# This script should show how to request prices, splits, and dividend data from Yahoo for a tkr.

echo busy...

cd ~/tkrapi20/
. env.bash

mkdir -p $TKRCSVD $TKRCSVH $TKRCSVS

TKR=IBM
$PYTHON ${PYTHONPATH}/request_tkr.py $TKR
# I should remove null-strings:
sed -i '/null/d' ${TKRCSVH}/${TKR}.csv
set -x
ls -la ${TKRCSVH}/${TKR}.csv
head   ${TKRCSVH}/${TKR}.csv
tail   ${TKRCSVH}/${TKR}.csv
cat    ${TKRCSVD}/${TKR}.csv
cat    ${TKRCSVS}/${TKR}.csv
exit
