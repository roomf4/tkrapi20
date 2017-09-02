# env.bash

# This file should help me set some env variables.
# I intend to 'dot' this file, not run it.
# Demo:
# . env.bash

export DATABASE_URL='postgres://tkrapi:tkrapi@127.0.0.1/tkrapi'
export PGURL='postgres://tkrapi:tkrapi@127.0.0.1/tkrapi'
export PYTHON=${HOME}/anaconda3/bin/python
export PARPATH=${HOME}/tkrapi20
export PYTHONPATH=${PARPATH}/py
export SCRIPTPATH=${PARPATH}/bin
export TKRCSV=${HOME}'/tkrcsv'
export TKRCSVD=${TKRCSV}'/div'
export TKRCSVH=${TKRCSV}'/history'
export TKRCSVS=${TKRCSV}'/split'
export FLASK_DEBUG=1
export PORT=5011
export KERAS_BACKEND=tensorflow
export PATH=${HOME}/anaconda3/bin:$PATH
# app, tkrapi20 for now:
export HPGURL=postgres://hpgygqtixbpwjf:70f594f2097cda735a7586cdd9b7133836d04fd6c5781c2a7314a957a94af2ab@ec2-54-163-233-201.compute-1.amazonaws.com:5432/d2nebmdp327bn5
# Note that I can assume the above variables do not exist in my heroku env.
# There, however, I might need to set PYTHONPATH.
export DB_URL=postgresql-spherical-15829
