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
pdb.set_trace()

# I should connect to local db, not Heroku:
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()
# I should drop the table I am about to fill:
sql_s = 'DROP TABLE IF EXISTS predictions2'
conn.execute(sql_s)
# I should loop through rows in the predictions table:
sql_s = '''SELECT
tkr,yrs,mnth,features,csv
FROM predictions
ORDER BY tkr,yrs,mnth,features
LIMIT 22
'''
result = conn.execute(sql_s)
if not result.rowcount:
  'return None'

for row in result:
  # I should access the CSV data in each row:
  pred_df = pd.read_csv(io.StringIO(row.csv))
  # I should add columns which could be used as a concat-key:
  pred_df['tkr']  = row.tkr
  pred_df['yrs']  = row.yrs
  pred_df['mnth'] = row.mnth
  pred_df['features'] = row.features
  pred_df.to_sql('predictions2', conn.engine, index=False, if_exists='append')
'return True'

# Now I should use SQL scripts to run reports:
# bin/psql.bash -f sql/rpt_pred.sql

'bye'
