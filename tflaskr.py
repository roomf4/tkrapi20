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

class Demo11(fr.Resource):
  """
  This class should be a simple syntax demo.
  """
  def get(self):
    my_k_s = 'hello'
    my_v_s = 'world'
    return {my_k_s: my_v_s}

api.add_resource(Demo11,   '/demo11.json')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5013))
  application.run(host='0.0.0.0', port=port)
'bye'

