"""
demoload_keras_fromdb.py

This script should demonstrate how to 
use Keras how to learn and predict by calling:
kerastkr.learn_predict_keraslinear()
And it shows how to load a model into a DB row by calling:
pgdb.predictions2db()
And it it shows how to feed a model from a DB row into keras.models.load_model()
Finally, it shows how to generate predictions from xtest_a fed to that model.

Demo:
. ../env.bash
~/anaconda3/bin/python demoload_keras_fromdb.py

"""

import kerastkr
import pdb

# pdb.set_trace()
out_df = kerastkr.load_predict_keraslinear(tkr='FB'
                                           ,yrs=4
                                           ,mnth='2017-10'
                                           ,features='pct_lag1,slope4,moy')
# I should see a DF with about 21 rows:
print(out_df)

'bye'
