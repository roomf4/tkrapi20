"""
requestem.py

This script should send some test-requests.

Demo:
. ../env.bash
$PYTHON requestem.py
"""

import requests
print('Busy...')

def request_this(url_s):
  response_r = requests.get(url_s)
  if (response_r.status_code > 200):
    print(url_s,response_r.status_code)

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

print('No news is probably good news.')
print('Done')
'bye'
