#!/bin/bash

# predictfrom_mlmodels.bash

# This script should demo how to generate predictions from mlmodels table.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash

$PYTHON py/predictfrom_mlmodels.py

exit
