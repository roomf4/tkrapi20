#!/bin/bash

# csv2db.bash

# This script should insert csv files into a table.
# This script will hang if the FlaskRESTful server is running.
# So I should shutdown the server before I run this script.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../

. env.bash
bin/rmbad_cookies.bash
$PYTHON py/csv2db.py

exit
