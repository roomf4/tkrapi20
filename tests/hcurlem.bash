#!/bin/bash

# hcurlem.bash

# This script should use curl to run some simple tests against tkrapi20.herokuapp.com

curl -v tkrapi20.herokuapp.com/demo11.json    > /tmp/test10.txt
curl -v tkrapi20.herokuapp.com/features       > /tmp/test13.txt

exit

curl -v tkrapi20.herokuapp.com/tkrinfo/AAPL   > /tmp/test14.txt
curl -v tkrapi20.herokuapp.com/tkrlist        > /tmp/test15.txt
curl -v tkrapi20.herokuapp.com/tkrs           > /tmp/test16.txt
curl -v tkrapi20.herokuapp.com/istkr/AAPL     > /tmp/test17.txt
curl -v tkrapi20.herokuapp.com/tkrprices/AAPL > /tmp/test18.txt
curl -v tkrapi20.herokuapp.com/dbtkrs         > /tmp/test19.txt

curl -v "tkrapi20.herokuapp.com/db/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test30.txt
curl -v "tkrapi20.herokuapp.com/dbyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test31.txt
curl -v "tkrapi20.herokuapp.com/dbtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test32.txt

curl -v "tkrapi20.herokuapp.com/db/keraslinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test33.txt
curl -v "tkrapi20.herokuapp.com/dbyr/keraslinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test34.txt
curl -v "tkrapi20.herokuapp.com/dbtkr/keraslinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test35.txt

curl -v "tkrapi20.herokuapp.com/db/kerasnn/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test36.txt
curl -v "tkrapi20.herokuapp.com/dbyr/kerasnn/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test37.txt
curl -v "tkrapi20.herokuapp.com/dbtkr/kerasnn/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test38.txt

curl -v tkrapi20.herokuapp.com/prediction_counts     > /tmp/test40.txt
curl -v tkrapi20.herokuapp.com/prediction_dimensions > /tmp/test41.txt
curl -v tkrapi20.herokuapp.com/kerasnn_dimensions    > /tmp/test42.txt

curl -v tkrapi20.herokuapp.com/sklinear/FB/3/2017-08/'pct_lag1,slope3,dow,moy'                > /tmp/test21.txt
curl -v "tkrapi20.herokuapp.com/csv/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test50.txt
curl -v "tkrapi20.herokuapp.com/csv/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test51.txt

curl -v "tkrapi20.herokuapp.com/csvyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"            > /tmp/test52.txt
curl -v "tkrapi20.herokuapp.com/csvtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"                > /tmp/test53.txt

exit
