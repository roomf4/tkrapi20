#!/bin/bash

# genf.bash

# This script should generate features from dates and prices.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash
$PYTHON py/genf.py

exit
