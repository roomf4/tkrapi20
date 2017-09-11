#!/bin/bash

# cr_models.bash

# This script should insert many models into mlmodels table.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash
$PYTHON py/cr_models.py

exit

