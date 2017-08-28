"""
requestem.py

This script should send some test-requests.

Demo:
. ../env.bash
$PYTHON requestem.py
"""

import requests
print('Busy...')

def request_this(url_s, params={'hl':2,'neurons':4}):
  response_r = requests.get(url_s, params)
  if (response_r.status_code > 200):
    print(url_s,response_r.status_code)

features_s = 'pct_lag1,slope3,dow,moy'
params     = {'features':features_s, 'hl': 2,'neurons':4}

request_this('http://localhost:5011/demos')
request_this('http://localhost:5011/algo_demos')
request_this('http://localhost:5011/demos')
request_this('http://localhost:5011/features')
request_this('http://localhost:5011/tkrinfo/AAPL')
request_this('http://localhost:5011/tkrlist')
request_this('http://localhost:5011/tkrs')
request_this('http://localhost:5011/istkr/AAPL')
request_this('http://localhost:5011/tkrprices/AAP')
request_this('http://localhost:5011/dbtkrs')

request_this("http://localhost:5011/sklinear/FB/3/2017-08/"+features_s)
request_this("http://localhost:5011/sklinear_yr/FB/3/2017/"+features_s)
request_this("http://localhost:5011/sklinear_tkr/FB/3/"+features_s)

request_this("http://localhost:5011/keraslinear/FB/3/2017-08/"+features_s)
request_this("http://localhost:5011/keraslinear_yr/FB/3/2017/"+features_s)
request_this("http://localhost:5011/keraslinear_tkr/FB/3/"+features_s)

request_this("http://localhost:5011/keras_nn/FB/3/2017-08", params)
request_this("http://localhost:5011/keras_nn_yr/FB/3/2017", params)
request_this("http://localhost:5011/keras_nn_tkr/FB/3"    , params)

request_this("http://localhost:5011/db/sklinear/FB/3/2017-08", params)
request_this("http://localhost:5011/dbyr/sklinear/FB/3/2017" , params)
request_this("http://localhost:5011/dbtkr/sklinear/FB/3"     , params)

request_this("http://localhost:5011/db/keraslinear/FB/3/2017-08", params)
request_this("http://localhost:5011/dbyr/keraslinear/FB/3/2017" , params)
request_this("http://localhost:5011/dbtkr/keraslinear/FB/3"     , params)

request_this("http://localhost:5011/db/keras_nn/FB/3/2017-08", params)
request_this("http://localhost:5011/dbyr/keras_nn/FB/3/2017" , params)
request_this("http://localhost:5011/dbtkr/keras_nn/FB/3"     , params)

print('No news is probably good news.')
print('Done')
'bye'
