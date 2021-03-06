#!/bin/bash

# curlem.bash

# This script should use curl to run some simple tests.

curl -v localhost:5011/demo11.json    > /tmp/test10.txt
curl -v localhost:5011/algo_demos     > /tmp/test11.txt
curl -v localhost:5011/demos          > /tmp/test12.txt
curl -v localhost:5011/features       > /tmp/test13.txt
curl -v localhost:5011/tkrinfo/AAPL   > /tmp/test14.txt
curl -v localhost:5011/tkrlist        > /tmp/test15.txt
curl -v localhost:5011/tkrs           > /tmp/test16.txt
curl -v localhost:5011/istkr/AAPL     > /tmp/test17.txt
curl -v localhost:5011/tkrprices/AAPL > /tmp/test18.txt
curl -v localhost:5011/dbtkrs         > /tmp/test19.txt

# I should test actual algos:
curl -v localhost:5011/sklinear/FB/3/2017-08/'pct_lag1,slope3,dow,moy'                       > /tmp/test21.txt
curl -v localhost:5011/sklinear_yr/FB/3/2017/'pct_lag1,slope3,dow,moy'                       > /tmp/test22.txt
curl -v localhost:5011/sklinear_tkr/FB/3/'pct_lag1,slope3,dow,moy'                           > /tmp/test23.txt
curl -v localhost:5011/keraslinear/FB/3/2017-08/'pct_lag2,slope5,moy'                        > /tmp/test24.txt
curl -v localhost:5011/keraslinear_yr/FB/3/2017/'pct_lag1,slope3,dow,moy'                    > /tmp/test25.txt
curl -v localhost:5011/keraslinear_tkr/FB/3/'pct_lag1,slope3,dow,moy'                        > /tmp/test26.txt
curl -v localhost:5011"/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test27.txt
# slow curl -v localhost:5011"/kerasnn_yr/FB/3/2017?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test28.txt
# slow curl -v localhost:5011"/kerasnn_tkr/FB/3?features='pct_lag1,slope4,moy'&hl=2&neurons=4"     > /tmp/test29.txt

curl -v "localhost:5011/db/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test30.txt
curl -v "localhost:5011/dbyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test31.txt
curl -v "localhost:5011/dbtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test32.txt

curl -v "localhost:5011/db/keraslinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test33.txt
curl -v "localhost:5011/dbyr/keraslinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test34.txt
curl -v "localhost:5011/dbtkr/keraslinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test35.txt

curl -v "localhost:5011/db/kerasnn/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test36.txt
curl -v "localhost:5011/dbyr/kerasnn/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/test37.txt
curl -v "localhost:5011/dbtkr/kerasnn/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/test38.txt

curl -v localhost:5011/prediction_counts     > /tmp/test40.txt
curl -v localhost:5011/prediction_dimensions > /tmp/test41.txt
curl -v localhost:5011/kerasnn_dimensions    > /tmp/test42.txt

curl -v "localhost:5011/csv/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/test50.txt
curl -v "localhost:5011/csv/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/test51.txt

curl -v "localhost:5011/csvyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"            > /tmp/test52.txt
curl -v "localhost:5011/csvtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"                > /tmp/test53.txt
curl -v "localhost:5011/csvtkr/keraslinear/FB/3?features='pct_lag1,slope3,dow,moy'"             > /tmp/test54.txt

exit
