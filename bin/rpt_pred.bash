#!/bin/bash

# rpt_pred.bash

# This script should report on predictions in predictions2 table.

# Demo:
# bin/rpt_pred.bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

echo $0 Busy...
echo Time now:
date
$PYTHON ${PYTHONPATH}/rpt_pred.py
echo $0 Done
date

exit
