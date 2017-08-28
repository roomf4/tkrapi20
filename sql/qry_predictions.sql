--
-- qry_predictions.sql
--

-- This script should help me query predictions.

-- Demo:
-- ../bin/psql.bash -f qry_predictions.sql

select tkr, count(tkr) count_tkr
from predictions
group by tkr
order by tkr
;

select tkr,yrs,mnth, count(tkr) count_tkr
from predictions
group by tkr,yrs,mnth
order by tkr,yrs,mnth
;


select
tkr
,yrs                   training_yrs
,features              feature_group
,substring(mnth for 4) yr
,count(tkr)            count_tkr
from predictions
group by tkr,yrs,features,substring(mnth for 4)
order by tkr,yrs,features,substring(mnth for 4)
;

