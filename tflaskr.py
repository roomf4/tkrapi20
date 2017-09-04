"""
tflaskr.py

Demo:
. env.bash
$PYTHON tflaskr.py
Other shell:
curl localhost:5013/demo11.json
"""

import io
import os
import datetime      as dt
import flask         as fl
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
# modules in the py folder:
import pgdb
import flaskclasses as flc

# I should ready flask_restful:
application = fl.Flask(__name__)
api         = fr.Api(application)

# I should setup CSV paths:

@api.representation('text/csv')
# ref:
# http://flask-restful.readthedocs.io/en/0.3.5/extending.html#response-formats
def output_csv(csv_data,code
               ,csvf_s # filename to serve
               ):
  """This function helps return a csv-string as a csv-file."""
  headers = {"Content-disposition":"attachment; filename="+csvf_s
               ,"Content-Type"    : "text/csv; charset=utf-8"}
  resp    = fl.make_response(csv_data, code, headers)
  return resp

class MyCSV(fr.Resource):
  """
  Returns some csv.
  """
  def get(self):
    somecsv_s = "a,b,c\n1.1,2.2,3.3\n1.1,2.2,3.3\n"
    respcode_i = 200
    return output_csv(somecsv_s, respcode_i, 'my.csv')

class TkrpricesCSV(fr.Resource):
  """
  Returns csv for a tkr from tkrprices table.
  """
  def get(self,tkr):
    respcode_i = 200
    tkrcsv_s   = pgdb.tkrpricesCSV(tkr)
    return output_csv(tkrcsv_s, respcode_i, tkr.upper()+'.csv')

class FeaturesCSV(fr.Resource):
  """
  Returns csv of features for a tkr from features table.
  """
  def get(self,tkr):
    respcode_i = 200
    csv_s   = pgdb.featuresCSV(tkr)
    return output_csv(csv_s, respcode_i, tkr.upper()+'.csv')


def gethelper(tkr,yrs):
  """This function should make syntax in get() calls more DRY."""
  features0_s = fl.request.args.get('features','pct_lag1,slope4,dow')
  features1_s = features0_s.replace("'","").replace('"','')
  features2_s = pgdb.check_features(features1_s) # needed for query
  features3_s = features2_s.replace(",","_")     # needed for filename
  tkru_s      = tkr.upper()
  yrs_s       = str(yrs)
  hl_s        = fl.request.args.get('hl',      '2') # default 2
  neurons_s   = fl.request.args.get('neurons', '4') # default 4
  hl_i        = int(hl_s)
  neurons_i   = int(neurons_s)
  algo_params_s = str([hl_i, neurons_i])
  return features2_s,features3_s,tkru_s,yrs_s,hl_s,neurons_s,algo_params_s

class Csv(fr.Resource):
  """
  Returns csv of predictions from predictions table.
  """
  def get(self,algo,tkr,yrs,mnth):
    features2_s,features3_s,tkru_s,yrs_s,hl_s,neurons_s,algo_params_s = gethelper(tkr,yrs)
    # I should get predictions from db:
    out_df = pgdb.dbpredictions(algo,tkru_s,yrs_s,mnth,features2_s,algo_params_s)
    csv_s  = out_df.to_csv(index=False,float_format='%.3f')
    # I should serve them:
    if (algo == 'kerasnn'):
      fn_s = '_'.join([tkru_s, algo, yrs_s, mnth, features3_s, hl_s, neurons_s])
    else: # I dont need hidden layers and neurons:
      fn_s = '_'.join([tkru_s, algo, yrs_s, mnth, features3_s])
    respcode_i = 200 # Means successful response.
    return output_csv(csv_s, respcode_i, fn_s + '.csv')

class CsvYr(fr.Resource):
  """
  Returns csv of predictions from predictions table.
  """
  def get(self,algo,tkr,yrs,yr):
    features2_s,features3_s,tkru_s,yrs_s,hl_s,neurons_s,algo_params_s = gethelper(tkr,yrs)
    # I should get predictions from db:
    yr_s   = str(yr)
    out_df = pgdb.dbpredictions_yr(algo,tkru_s,yrs_s,yr_s,features2_s,algo_params_s)
    csv_s  = out_df.to_csv(index=False,float_format='%.3f')
    # I should serve them:
    if (algo == 'kerasnn'):
      fn_s = '_'.join([tkru_s, algo, yrs_s, yr_s, features3_s, hl_s, neurons_s])
    else: # I dont need hidden layers and neurons:
      fn_s = '_'.join([tkru_s, algo, yrs_s, yr_s, features3_s])
    respcode_i = 200 # Means successful response.
    return output_csv(csv_s, respcode_i, fn_s + '.csv')

class CsvTkr(fr.Resource):
  """
  Returns csv of predictions from predictions table.
  """
  def get(self,algo,tkr,yrs):
    features2_s,features3_s,tkru_s,yrs_s,hl_s,neurons_s,algo_params_s = gethelper(tkr,yrs)
    # I should get predictions from db:
    out_df = pgdb.dbpredictions_tkr(algo,tkru_s,yrs_s,features2_s,algo_params_s)
    csv_s  = out_df.to_csv(index=False,float_format='%.3f')
    # I should serve them:
    if (algo == 'kerasnn'):
      fn_s = '_'.join([tkru_s, algo, yrs_s, features3_s, hl_s, neurons_s])
    else: # I dont need hidden layers and neurons:
      fn_s = '_'.join([tkru_s, algo, yrs_s, features3_s])
    respcode_i = 200 # Means successful response.
    return output_csv(csv_s, respcode_i, fn_s + '.csv')

# Should be CSV classes above this line, resources below:

api.add_resource(MyCSV        ,'/my.csv')
api.add_resource(TkrpricesCSV ,'/tkrprices/<tkr>'+'.csv')
api.add_resource(FeaturesCSV  ,'/features/<tkr>'+'.csv')
api.add_resource(Csv,    '/csv/<algo>/<tkr>/<int:yrs>/<mnth>')
api.add_resource(CsvYr,  '/csvyr/<algo>/<tkr>/<int:yrs>/<int:yr>')
api.add_resource(CsvTkr, '/csvtkr/<algo>/<tkr>/<int:yrs>')

#api.add_resource(flc.Demo11,   '/demo11.json')
# api.add_resource(flc.Features, '/features')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5013))
  application.run(host='0.0.0.0', port=port)
'bye'

