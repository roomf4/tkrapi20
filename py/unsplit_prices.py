"""
unsplit_prices.py

This script should create a column named uscp which I see as unsplit_prices.

Given a splitdate, this script should find all prices at and after the splitdate.
Then uscp should be made from (cp * split_ratio).

Demo:
. env.bash
$PYTHON py/unsplit_prices.py
"""

import io
import os
import pdb
import pandas     as pd
import sqlalchemy as sql
from   fractions import Fraction

# I should connect to the db.
db_s = os.environ['PGURL']
conn = sql.create_engine(db_s).connect()

# I should loop through the table full of tkrs, prices, splitdates:
sql_s   = "select tkr, csvh, csvs from tkrprices order by tkr" # where tkr like 'AA%'"
sql_sql = sql.text(sql_s)
result  = conn.execute(sql_sql)
if not result.rowcount:
  sys.exit(1)

for rowtkr in result:
  print(rowtkr.tkr)
  cp_df = pd.read_csv(io.StringIO(rowtkr.csvh),names=('cdate','cp'))
  sd_df = pd.read_csv(io.StringIO(rowtkr.csvs),names=('sdate','ratio'))
  # I should initialize unsplit prices to current prices:
  cp_df['uscp'] = cp_df.cp
  # For each tkr, the split dates should drive a loop:
  for rowsd in sd_df.itertuples():
    pdb.set_trace()
    # I should create a Series full of Booleans:
    dt_gte_sd_sr = (cp_df.cdate >= rowsd.sdate)
    # Above series tells me dates after splitdate.
    # Prices after splitdate should be multiplied by splitratio.
    cp_df.loc[dt_gte_sd_sr,'uscp'] = float(Fraction(rowsd.ratio)) * cp_df[dt_gte_sd_sr].uscp
    dt_gte_sd_sr.head()
    dt_gte_sd_sr.tail()
    print(rowsd.sdate)

'bye'
