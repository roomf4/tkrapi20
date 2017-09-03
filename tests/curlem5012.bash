#!/bin/bash

# curlem5012.bash

# This script should use curl to run some simple tests.

curl -v localhost:5012/demo11.json    > /tmp/test10.txt
curl -v localhost:5012/features       > /tmp/test13.txt

curl -v localhost:5012/tkrinfo/AAPL   > /tmp/test14.txt
curl -v localhost:5012/tkrlist        > /tmp/test15.txt
curl -v localhost:5012/tkrs           > /tmp/test16.txt
curl -v localhost:5012/istkr/AAPL     > /tmp/test17.txt
curl -v localhost:5012/tkrprices/AAPL > /tmp/test18.txt
curl -v localhost:5012/dbtkrs         > /tmp/test19.txt

exit
# I should test actual algos:
curl -v localhost:5012/sklinear/FB/3/2017-08/'pct_lag1,slope3,dow,moy'                       > /tmp/test21.txt
curl -v localhost:5012/sklinear_yr/FB/3/2017/'pct_lag1,slope3,dow,moy'                       > /tmp/test22.txt
curl -v localhost:5012/sklinear_tkr/FB/3/'pct_lag1,slope3,dow,moy'                           > /tmp/test23.txt
curl -v localhost:5012/keraslinear/FB/3/2017-08/'pct_lag2,slope5,moy'                        > /tmp/test24.txt
curl -v localhost:5012/keraslinear_yr/FB/3/2017/'pct_lag1,slope3,dow,moy'                    > /tmp/test25.txt
curl -v localhost:5012/keraslinear_tkr/FB/3/'pct_lag1,slope3,dow,moy'                        > /tmp/test26.txt
curl -v localhost:5012"/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test27.txt
# slow curl -v localhost:5012"/kerasnn_yr/FB/3/2017?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test28.txt
# slow curl -v localhost:5012"/kerasnn_tkr/FB/3?features='pct_lag1,slope4,moy'&hl=2&neurons=4"     > /tmp/test29.txt

curl -v "localhost:5012/db/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test30.txt
curl -v "localhost:5012/dbyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test31.txt
curl -v "localhost:5012/dbtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test32.txt

curl -v "localhost:5012/db/keraslinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test33.txt
curl -v "localhost:5012/dbyr/keraslinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test34.txt
curl -v "localhost:5012/dbtkr/keraslinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test35.txt

curl -v "localhost:5012/db/kerasnn/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test36.txt
curl -v "localhost:5012/dbyr/kerasnn/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test37.txt
curl -v "localhost:5012/dbtkr/kerasnn/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test38.txt

curl -v localhost:5012/prediction_counts     > /tmp/test40.txt
curl -v localhost:5012/prediction_dimensions > /tmp/test41.txt
curl -v localhost:5012/kerasnn_dimensions    > /tmp/test42.txt

curl -v localhost:5012/sklinear/FB/3/2017-08/'pct_lag1,slope3,dow,moy'                > /tmp/test21.txt
curl -v "localhost:5012/csv/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test50.txt
curl -v "localhost:5012/csv/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test51.txt

curl -v "localhost:5012/csvyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"            > /tmp/test52.txt
curl -v "localhost:5012/csvtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"                > /tmp/test53.txt

exit
