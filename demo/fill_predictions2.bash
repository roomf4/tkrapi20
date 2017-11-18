#!/bin/bash

# ~/tkrapi20/demo/fill_predictions2.bash

# This script should copy rows out of predictions table into a DataFrame.
# Each row in predictions contains about 21 predictions.
# Then it should transform that DataFrame into a table named predictions2.
# Each row in predictions2 contains one prediction.

# After predictions2 is loaded, it can be used for reporting.

# Here is a query I like to run against predictions2:
# SELECT tkr, SUM(pct_lead),SUM(effectiveness)
# FROM predictions2 GROUP BY tkr ORDER BY tkr;

echo busy...
cd ~/tkrapi20/
. env.bash
echo calling py/fill_predictions2.py
~/anaconda3/bin/python py/fill_predictions2.py
echo Python done.

echo calling psql.bash

bin/psql.bash<<EOF
SELECT
tkr
,SUM(pct_lead)sum_pct_lead
,SUM(effectiveness)sum_effectiveness
FROM predictions2 GROUP BY tkr ORDER BY tkr;
EOF

exit
