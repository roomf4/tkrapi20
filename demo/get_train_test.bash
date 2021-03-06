#!/bin/bash

# ~/tkrapi20/demo/get_train_test.bash

# This script should demo how to call pgdb.get_train_test()
# which is a method I use to get data ready for training and testing.

cd ~/tkrapi20/
. env.bash

~/anaconda3/bin/python <<EOF
import pgdb
tkr        = 'FB'
yrs        = 4
mnth       = '2017-10'
features_s = 'pct_lag1,slope4,moy'
xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,yrs,mnth,features_s)
print(xtrain_a[:9])
print(ytrain_a[:9])
print(xtest_a)
print(out_df)
EOF

exit
exit
exit

# I should see something like this:

dan@tkrapi:~/tkrapi20/demo $ ./get_train_test.bash
Using TensorFlow backend.
[[ 0.09  -1.971  0.884]
 [ 0.1    0.378  0.475]
 [ 0.1   -0.278 -0.054]
 [ 0.1   -2.188 -1.029]
 [ 0.1    3.782  0.403]
 [ 0.1   -1.019  0.05 ]
 [ 0.1   -6.69  -1.587]
 [ 0.1   -0.785 -1.233]
 [ 0.1    4.875 -1.029]]
[0.37799999999999995 -0.278 -2.188 3.782 -1.0190000000000001 -6.69 -0.785
 4.875 0.122]
[[ 0.1   -0.819  0.777]
 [ 0.1    0.289  0.336]
 [ 0.1   -0.906 -0.046]
 [ 0.1    1.674  0.054]
 [ 0.1    0.578  0.405]
 [ 0.1    0.157  0.371]
 [ 0.1   -0.528  0.461]
 [ 0.1    0.67   0.218]
 [ 0.1   -0.11   0.046]
 [ 0.1    0.69   0.18 ]
 [ 0.1    0.449  0.422]
 [ 0.1    0.911  0.484]
 [ 0.1   -0.045  0.497]
 [ 0.1   -0.835  0.117]
 [ 0.1    0.241  0.066]
 [ 0.1   -2.12  -0.695]
 [ 0.1    0.309 -0.611]
 [ 0.1   -0.698 -0.575]
 [ 0.1    0.018 -0.636]
 [ 0.1    4.249  0.957]
 [ 0.1    1.119  1.155]
 [ 0.1    0.106  1.335]]
           cdate      cp  pct_lead
1351  2017-10-02  169.47     0.289
1352  2017-10-03  169.96    -0.906
1353  2017-10-04  168.42     1.674
1354  2017-10-05  171.24     0.578
1355  2017-10-06  172.23     0.157
1356  2017-10-09  172.50    -0.528
1357  2017-10-10  171.59     0.670
1358  2017-10-11  172.74    -0.110
1359  2017-10-12  172.55     0.690
1360  2017-10-13  173.74     0.449
1361  2017-10-16  174.52     0.911
1362  2017-10-17  176.11    -0.045
1363  2017-10-18  176.03    -0.835
1364  2017-10-19  174.56     0.241
1365  2017-10-20  174.98    -2.120
1366  2017-10-23  171.27     0.309
1367  2017-10-24  171.80    -0.698
1368  2017-10-25  170.60     0.018
1369  2017-10-26  170.63     4.249
1370  2017-10-27  177.88     1.119
1371  2017-10-30  179.87     0.106
1372  2017-10-31  180.06     1.444
dan@tkrapi:~/tkrapi20/demo $ 
dan@tkrapi:~/tkrapi20/demo $ 
dan@tkrapi:~/tkrapi20/demo $ 
