#!/bin/bash

# rpt_pred.bash

# This script should copy predictions into predictions2 and then report.

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
