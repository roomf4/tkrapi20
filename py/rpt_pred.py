"""
rpt_pred.py

This script should copy predictions in DataFrames into predictions2 table.

Demo:
$PYTHON ${PYTHONPATH}/rpt_pred.py
"""

import io
import os
import pdb
import datetime      as dt
import pandas        as pd
import sqlalchemy    as sql
# modules in the py folder:
import pgdb


# I should loop through rows in the predictions table:
db_s = os.environ['PGURL'] # s.b. local db not Heroku.
conn = sql.create_engine(db_s).connect()
sql_s  = '''SELECT
tkr,yrs,mnth,features,csv
FROM predictions
ORDER BY tkr,yrs,mnth,features
LIMIT 22
'''

result = conn.execute(sql_s)
if not result.rowcount:
  'return None'

for row in result:
  pred_df = pd.read_csv(io.StringIO(row.csv))
'return True'

'bye'
