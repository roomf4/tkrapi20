"""
dropout_study.py

This script should study keras dropout layers.

Demo:
python dropout_study.py
"""

import io
import pdb
import os
import flask
import datetime      as dt
import flask_restful as fr
import numpy         as np
import pandas        as pd
import sqlalchemy    as sql
import keras
# modules in the py folder:
import pgdb

# https://keras.io/models/model/#methods
batch_size_i = 256 # Doc: Number of samples per gradient update.
epochs_i     = 2 # Doc: Number of epochs to train the model.

def learn_predict_keraslinear(tkr='FB',yrs=4,mnth='2017-08',dropout=True):
  """This function should use keras to learn, predict."""
  features_l = pgdb.getfeatures()
  features_s =','.join(sorted(features_l))
  # I should get train, test data.
  # Also get copy of test data in a DataFrame for later reporting:
  xtrain_a, ytrain_a, xtest_a, out_df = pgdb.get_train_test(tkr,yrs,mnth,features_s)
  if ((xtrain_a.size == 0) or (ytrain_a.size == 0) or (xtest_a.size == 0)):
    return out_df # probably empty too.
  # Start using Keras here.
  kmodel     = keras.models.Sequential()
  # I should fit a Keras model to xtrain_a, ytrain_a
  features_l = features_s.split(',')
  features_i = len(features_l)
  kmodel.add(keras.layers.core.Dense(features_i, input_shape=(features_i,)))
  # https://keras.io/activations/
  kmodel.add(keras.layers.core.Activation('linear'))
  if dropout:
    # Activations should have 'Dropout' to reduce overfitting:
    kmodel.add(keras.layers.core.Dropout(0.1))
    #
  # I should have 1 linear-output:
  kmodel.add(keras.layers.core.Dense(1)) 
  kmodel.add(keras.layers.core.Activation('linear'))
  kmodel.compile(loss='mean_squared_error', optimizer='adam')
  kmodel.fit(xtrain_a,ytrain_a, batch_size=batch_size_i, epochs=epochs_i)
  # I should predict xtest_a then update out_df
  predictions_a           = np.round(kmodel.predict(xtest_a),3)
  # Done with Keras, I should pass along the predictions.
  predictions_l           = [p_f[0] for p_f in predictions_a] # I want a list
  out_df['prediction']    = predictions_l
  out_df['effectiveness'] = np.sign(out_df.pct_lead*out_df.prediction)*np.abs(out_df.pct_lead)
  out_df['accuracy']      = (1+np.sign(out_df.effectiveness))/2
  algo                    = 'keraslinear'
  # I should save predictions:
  dfcsv_s = os.environ['HOME']+'/dfcsv'
  csvn_s  = dfcsv_s+'/dropout_'+str(dropout)+'/predictions.csv'  
  out_df.to_csv(csvn_s,index=False,float_format='%.3f')
  # I should return a DataFrame useful for reporting on the predictions.
  return out_df

out_df = learn_predict_keraslinear('FB',4,'2017-08',False)
print(out_df)

'bye'
