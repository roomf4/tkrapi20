"""
flask4js.py

This script should run a flask server which serves static HTML and JS.

Demo:
echo hello > static/ur.html
export FLASK_DEBUG=1
python flask4js.py
curl 127.0.0.1:5000/static/.html
"""

import os
from   flask import Flask
application = Flask(__name__)
                               
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
'bye'

