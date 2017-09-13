--
-- qry_mlmodels.sql
--

-- This script should query table: mlmodels

select tkr,algo,count(tkr) count_tkr
from mlmodels
group by tkr,algo
order by tkr,algo
;
