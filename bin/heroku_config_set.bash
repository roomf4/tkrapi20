#!/bin/bash

# heroku_config_set.bash

# This script should set env variables for my heroku env.

heroku config:set DATABASE_URL=postgres://hpgygqtixbpwjf:70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab@ec2-54-163-233-201.compute-1.amazonaws.com:5432/d2nebmdp327bn5

heroku config:set PYTHONPATH=/app/py

exit
