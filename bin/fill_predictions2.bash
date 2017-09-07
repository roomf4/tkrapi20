#!/bin/bash

# fill_predictions2.bash

# This script should copy predictions into predictions2.

# Demo:
# bin/rpt_pred.bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

echo $0 Busy...
echo Time now:
date
$PYTHON ${PYTHONPATH}/fill_predictions2.py
echo $0 Done
date

exit
