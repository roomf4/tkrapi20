--
-- rpt_pred.sql
--

-- This script should query the predictions2 table.

SELECT COUNT(*) from predictions;
SELECT COUNT(*) from predictions2;

SELECT
tkr
,COUNT(tkr)
from predictions
GROUP BY tkr
ORDER BY tkr
;

SELECT
tkr
,COUNT(tkr)
from predictions2
GROUP BY tkr
ORDER BY tkr
;
