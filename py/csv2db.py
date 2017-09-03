"""
csv2db.py

This script should insert csv files into a table.

This script will hang if the FlaskRESTful server is running.
So I should shutdown the server before I run this script.

Demo:
. env.bash
$PYTHON py/csv2db.py
"""

import glob
import pdb
import os
import pandas     as pd
import sqlalchemy as sql

# I should connect to the DB
db_s = os.environ['DATABASE_URL']

conn = sql.create_engine(db_s).connect()

sql_s = "drop table if exists tkrprices"
conn.execute(sql_s)

sql_s = "create table tkrprices(tkr varchar, crtime timestamp, csvd text, csvh text, csvs text)"
conn.execute(sql_s)

# I should read csv files:
for csvf_s in sorted(glob.glob(os.environ['TKRCSVH']+'/*.csv')):
  # I should avoid files which are too small:
  sz_i = os.path.getsize(csvf_s)
  print(csvf_s, sz_i)
  if (sz_i > 2123):
    tkr_s   = csvf_s.split('/')[-1].split('.')[0] # should be something like 'IBM'
    csvh_df = pd.read_csv(csvf_s)
    # I should convert to String and pick only two columns:
    csvh_s = csvh_df.to_csv(index=False,header=False,columns=('Date','Close'),float_format='%.3f')
    # History should now be done. Dividends and Splits should be next:
    csvfd_s = os.environ['TKRCSVD']+'/'+tkr_s+'.csv'
    csvfs_s = os.environ['TKRCSVS']+'/'+tkr_s+'.csv'
    csvd_s  = pd.read_csv(csvfd_s).sort_values('Date').to_csv(index=False,header=False)
    csvs_s  = pd.read_csv(csvfs_s).sort_values('Date').to_csv(index=False,header=False)
    sql_s   = "insert into tkrprices(tkr,crtime,csvd,csvh,csvs)values(%s , now(), %s, %s, %s)"
    conn.execute(sql_s,[tkr_s, csvd_s, csvh_s, csvs_s] )

# I should check:
# sql_s = "select tkr, csvh from tkrprices limit 1"
# result = conn.execute(sql_s)
# 
# for row in result:
#     print(row['tkr'],row['csvh'].split(',')[-2:])

# I should check via shell:
# ../bin/psql.bash
# select       tkr  from tkrprices;
# select count(tkr) from tkrprices;
# select csvh from tkrprices where tkr='SNAP';
# select substring(csvh from 0 for 144) from tkrprices where tkr='SNAP';
# select tkr, substring(csvh from 0 for 22) from tkrprices;
# select tkr, csvs from tkrprices WHERE tkr = 'AAPL';
# select tkr, csvd from tkrprices WHERE tkr = 'AAPL';
'bye'

