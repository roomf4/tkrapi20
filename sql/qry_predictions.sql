--
-- qry_predictions.sql
--

-- This script should help me query predictions.

-- Demo:
-- ../bin/psql.bash -f qry_predictions.sql

-- This should help me notice recent predictions:
select
tkr
,algo
,yrs
,mnth
,features
,coef
,crtime
from predictions
-- mnth s.b. like '2017-09'
-- where mnth = substring(now()::varchar for 7)
order by crtime desc
limit 33
;

\q

-- This should help me notice recent predictions:
select tkr
,yrs
,substring(mnth for 4) yr
,features    feature_group
,count(tkr)  count_tkr
,min(crtime) min_crtime
,max(crtime) max_crtime
from predictions
group by tkr,yrs,substring(mnth for 4),features
order by max(crtime)
;
-- Above query returns too many rows after I generate many feature combinations.
\q

select tkr
,count(tkr)  count_tkr
,min(crtime) min_crtime
,max(crtime) max_crtime
from predictions
group by tkr
order by tkr
;

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

