"""
wsgi.py
This script should help me run flask-restful on heroku.
I usually dont use this script on my laptop.
"""
from hflaskr import application

if __name__ == "__main__":
    application.run()
