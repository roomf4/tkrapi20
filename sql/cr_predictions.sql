--
-- cr_predictions.sql
--

-- This script should create table predictions.

CREATE TABLE IF NOT EXISTS
predictions(
  tkr          VARCHAR
  ,yrs         INTEGER
  ,mnth        VARCHAR
  ,features    VARCHAR
  ,algo        VARCHAR
  ,algo_params VARCHAR
  ,crtime      TIMESTAMP
  ,sklinear_coef TEXT
  ,csv           TEXT
  ,kmodel_h5     BYTEA
);
  
