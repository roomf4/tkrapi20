#!/bin/bash

# rpt_pred.bash

# This script should copy predictions into predictions2 and then report.

# Demo:
# bin/rpt_pred.bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

$PYTHON ${PYTHONPATH}/rpt_pred.py

exit