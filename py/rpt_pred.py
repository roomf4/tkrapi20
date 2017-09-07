"""
rpt_pred.py

This script should report on predictions in predictions2 table.

Demo:
$PYTHON ${PYTHONPATH}/rpt_pred.py
"""

import io
import os
import pdb
import datetime      as dt
import pandas        as pd
import sqlalchemy    as sql

# I should connect to local db, not Heroku:
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()

# I should query:
sql_s = '''
SELECT
tkr
,SUM(pct_lead) sum_pct_lead
,MIN(cdate)    min_cdate
,MAX(cdate)    max_cdate
FROM predictions2
GROUP BY tkr
'''

# I should copy result into DF:
rpt_df = pd.read_sql(sql_s, conn)
print(rpt_df)

'bye'
