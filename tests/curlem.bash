#!/bin/bash

# curlem.bash

# This script should use curl to run some simple tests.

set -x

curl -v localhost:5011/demo11.json    > /tmp/test20.txt
curl -v localhost:5011/algo_demos     > /tmp/test21.txt
curl -v localhost:5011/demos	      > /tmp/test22.txt
curl -v localhost:5011/features	      > /tmp/test23.txt
curl -v localhost:5011/tkrinfo/AAPL   > /tmp/test24.txt
curl -v localhost:5011/tkrlist	      > /tmp/test25.txt
curl -v localhost:5011/tkrs	      > /tmp/test26.txt
curl -v localhost:5011/istkr/AAPL     > /tmp/test27.txt
curl -v localhost:5011/tkrprices/AAPL > /tmp/test28.txt

exit

curl -v localhost:5011/algo_demos                                                            > /tmp/test10.txt
curl -v localhost:5011/sklinear/FB/3/2017-08/'pct_lag1,slope3,dow,moy'                       > /tmp/test11.txt
curl -v localhost:5011/sklinear_yr/FB/2/2017/'pct_lag1,slope3,dow,moy'                       > /tmp/test12.txt
curl -v localhost:5011/sklinear_tkr/FB/2/'pct_lag1,slope3,dow,moy'                           > /tmp/test13.txt
curl -v localhost:5011/keraslinear/FB/3/2017-08/'pct_lag2,slope5,moy'                        > /tmp/test14.txt
curl -v localhost:5011/keraslinear_yr/FB/2/2017/'pct_lag1,slope3,dow,moy'                    > /tmp/test15.txt
curl -v localhost:5011/keraslinear_tkr/FB/2/'pct_lag1,slope3,dow,moy'                        > /tmp/test16.txt
curl -v localhost:5011"/keras_nn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test17.txt
curl -v localhost:5011"/keras_nn_yr/FB/3/2017?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test18.txt
curl -v localhost:5011"/keras_nn_tkr/FB/3?features='pct_lag1,slope4,moy'&hl=2&neurons=4"     > /tmp/test19.txt

exit
