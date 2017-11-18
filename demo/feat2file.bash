#!/bin/bash

# ~/tkrapi20/demo/feat2file.bash

# This script should demonstrate how to copy data out of a Postgres row into a CSV file.

cd ~/tkrapi20/

. env.bash

~/anaconda3/bin/python py/feat2file.py

head /tmp/featFB.csv

exit

# I should see something like this:

dan@tkrapi:~/tkrapi20 $ demo/feat2file.bash
Using TensorFlow backend.
Wrote: /tmp/featFB.csv
pgdb.getfeat2file('FB') done.
cdate,cp,pct_lead,pct_lag1,pct_lag2,pct_lag4,pct_lag8,slope3,slope4,slope5,slope6,slope7,slope8,slope9,dow,moy
2012-05-18,38.230,-10.986,0.000,0.000,0.000,0.000,,,,,,,,0.050,0.050
2012-05-21,34.030,-8.904,-10.986,0.000,0.000,0.000,,,,,,,,0.010,0.050
2012-05-22,31.000,3.226,-8.904,-18.912,0.000,0.000,,,,,,,,0.020,0.050
2012-05-23,32.000,3.219,3.226,-5.965,0.000,0.000,-6.421,,,,,,,0.030,0.050
2012-05-24,33.030,-3.391,3.219,6.548,-13.602,0.000,-1.041,-3.998,,,,,,0.040,0.050
2012-05-25,31.910,-9.621,-3.391,-0.281,-6.230,0.000,0.939,-1.657,-3.902,,,,,0.050,0.050
2012-05-29,28.840,-2.254,-9.621,-12.685,-6.968,0.000,-3.370,-1.717,-3.310,-4.921,,,,0.020,0.050
2012-05-30,28.190,5.002,-2.254,-11.658,-11.906,0.000,-5.442,-3.124,-1.825,-3.157,-4.584,,,0.030,0.050
2012-05-31,29.600,-6.351,5.002,2.635,-10.384,-22.574,-2.667,-2.894,-1.583,-0.763,-2.065,-3.471,,0.040,0.050
dan@tkrapi:~/tkrapi20 $ 
dan@tkrapi:~/tkrapi20 $
