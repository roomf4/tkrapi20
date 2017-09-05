--
-- qry_predictions.sql
--

-- This script should help me query predictions.

-- Demo:
-- ../bin/psql.bash -f qry_predictions.sql

select tkr
,count(tkr)  count_tkr
,min(crtime) min_crtime
,max(crtime) max_crtime
from predictions
group by tkr
order by tkr
;

\q

select tkr
,yrs
,mnth
,count(tkr)  count_tkr
,min(crtime) min_crtime
,max(crtime) max_crtime
from predictions
group by tkr,yrs,mnth
order by max(crtime)
;

\q

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
algo
,tkr
,yrs                   training_yrs
,features              feature_group
,substring(mnth for 4) yr
,count(tkr)            count_tkr
from predictions
group by algo,tkr,yrs,features,substring(mnth for 4)
order by algo,tkr,yrs,features,substring(mnth for 4)
;


select
algo_params
,tkr
,yrs                   training_yrs
,features              feature_group
,substring(mnth for 4) yr
,count(tkr)            count_tkr
from predictions
where algo = 'kerasnn'
group by algo,algo_params,tkr,yrs,features,substring(mnth for 4)
order by algo,algo_params,tkr,yrs,features,substring(mnth for 4)
;

