
import numpy as np

last3 = [        170.950, 173.510, 172.960]
last4 = [173.210,170.950, 173.510, 172.960]

lastmv = np.mean(last3)
mv4    = np.mean([173.210,170.950, 173.510])

slp = 100 * (lastmv -mv4 ) / lastmv
# s.b: -0.0483

# cdate     ,cp     ,pct_lead,pct_lag1,pct_lag2,pct_lag4,pct_lag8,slope3,slope4,slope5,slope6,slope7,slope8,slope9,dow  ,moy
# 2017-09-12,172.960,0.000   ,-0.317  ,1.176   ,0.506   ,1.789   ,-0.048,0.126 ,0.260 ,0.091 ,0.082 ,0.221 ,0.317 ,0.020,0.090
