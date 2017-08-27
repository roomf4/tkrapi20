#!/bin/bash

# flaskr.bash

# This script should start a Flask RESTful server.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH
. env.bash

$PYTHON flaskr.py

exit
