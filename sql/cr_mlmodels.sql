--
-- cr_mlmodels.sql
--

-- This script should create table mlmodels.

CREATE TABLE
mlmodels(
  tkr          VARCHAR
  ,yrs         INTEGER
  ,mnth        VARCHAR
  ,features    VARCHAR
  ,algo        VARCHAR
  ,algo_params VARCHAR
  ,crtime      TIMESTAMP
  ,sklinear_coef TEXT
  ,kmodel_h5     BYTEA
);
