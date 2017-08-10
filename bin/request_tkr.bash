#!/bin/bash

# request_tkr.bash

# This script should call request_tkr.py
# which should help me collect prices into CSV files

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
PARPATH=${SCRIPTPATH}/..
PYPATH=${PARPATH}/py

date
echo busy...
#cat ${PARPATH}/tkrs.txt|while read TKR
cat ${PARPATH}/tkrlist.txt|while read TKR
do
    echo busy with                  $TKR
    python ${PYPATH}/request_tkr.py $TKR
    gzip     /tmp/request_tkr/html/${TKR}.html
    gzip      /tmp/request_tkr/csv/${TKR}.csv
done
date

exit
