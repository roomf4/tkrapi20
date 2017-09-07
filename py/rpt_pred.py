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
# local:
import notf

# I should connect to local db, not Heroku:
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()
# I should declare GROUP BY columns:
gbcol_l  = ['tkr','yrs']
# I should get all combinations of them:
combos_l = notf.list2combos(gbcol_l)
for combo_tpl in combos_l:
  # I should convert tuples to strings:
  gbcols_s = ','.join(combo_tpl)
  # I should query:
  sql_s = '''
  SELECT
  {}
  ,SUM(pct_lead)      sum_pct_lead
  ,SUM(effectiveness) sum_effectiveness
  ,MIN(cdate)         min_cdate
  ,MAX(cdate)         max_cdate
  FROM predictions2
  GROUP BY {}
  ORDER BY {}
  '''.format(gbcols_s,gbcols_s,gbcols_s)
  print(sql_s)
  # I should copy result into DF:
  rpt_df = pd.read_sql(sql_s, conn)
  # I should report:
  print(rpt_df)
'bye'
