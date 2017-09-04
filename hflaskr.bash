#!/bin/bash

# hflaskr.bash

# This script should start a Flask RESTful server.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH
. env.bash
export PORT=5013

# This server should be a simple test.
$PYTHON hflaskr.py

exit
