#!/bin/bash

# req2db.bash

# This script should request prices and then load them into db.

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd ${SCRIPTPATH}/../
. env.bash

# I should request prices:
# ${SCRIPTPATH}/curl_tkrs.bash # bash, curl, and sed
${SCRIPTPATH}/request_tkr.bash # bash and Python

# I should rm bad csv files:
${SCRIPTPATH}/rmbad_cookies.bash

# I should load prices into db:
$PYTHON ${PYTHONPATH}/csv2db.py

# I should generate features and load them into db:
$PYTHON ${PYTHONPATH}/genf.py

exit
