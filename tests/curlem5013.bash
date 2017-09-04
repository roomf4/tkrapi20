#!/bin/bash

# curlem5013.bash

# This script should use curl to run some simple tests against lh:5013

curl -v lh:5013/my.csv    > /tmp/htest10.txt
curl -v "lh:5013/csv/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/htest50.txt
curl -v "lh:5013/csv/kerasnn/FB/3/2017-08?features='pct_lag1,slope4,moy'&hl=2&neurons=4" > /tmp/htest51.txt

curl -v "lh:5013/csvyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'" > /tmp/htest52.txt
curl -v "lh:5013/csvtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"     > /tmp/htest53.txt


curl -v lh:5013/demo11.json    > /tmp/htest09.txt
curl -v lh:5013/features       > /tmp/htest13.txt
curl -v lh:5013/tkrinfo/AAPL   > /tmp/htest14.txt
curl -v lh:5013/tkrlist        > /tmp/htest15.txt
curl -v lh:5013/tkrs           > /tmp/htest16.txt
curl -v lh:5013/istkr/AAPL     > /tmp/htest17.txt
curl -v lh:5013/tkrprices/AAPL > /tmp/htest18.txt
curl -v lh:5013/dbtkrs         > /tmp/htest19.txt

exit

# I should test predictions table:

curl -v "lh:5013/db/sklinear/FB/3/2017-08?features='pct_lag1,slope3,dow,moy'" > /tmp/htest30.txt

curl -v "lh:5013/dbyr/sklinear/FB/3/2017?features='pct_lag1,slope3,dow,moy'"  > /tmp/htest31.txt
curl -v "lh:5013/dbtkr/sklinear/FB/3?features='pct_lag1,slope3,dow,moy'"      > /tmp/htest32.txt

curl -v lh:5013/prediction_counts     > /tmp/htest40.txt
curl -v lh:5013/prediction_dimensions > /tmp/htest41.txt
curl -v lh:5013/kerasnn_dimensions    > /tmp/htest42.txt

exit



