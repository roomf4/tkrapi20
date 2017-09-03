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

# I should ready flask_restful:
application = fl.Flask(__name__)
api         = fr.Api(application)

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

