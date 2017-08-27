#!/bin/bash

# hflaskr.bash

# This script should start a Flask RESTful server.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH
. env.bash
export PORT=5012

# This server should get all data from db, not any from models:
$PYTHON hflaskr.py

exit
