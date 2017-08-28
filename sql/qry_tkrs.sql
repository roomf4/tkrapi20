--
-- qry_tkrs.sql
--

-- This script should help me count tkrs in different tables.

-- Demo:
-- ../bin/psql.bash -f qry_tkrs.sql

select       tkr  from tkrprices order by tkr;
select count(tkr) from tkrprices;
select count(tkr) from features;
select count(tkr) from predictions;

