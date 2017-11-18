#!/bin/bash

# This is a simple demo of Keras.

cd ~/tkrapi20/

. env.bash

# The script below shows the following features:
# - Create a 2 layer neural net
# - Build a model from that net
# - Collect predictions from the model
# - Save the model as an HDF5 file with an h5 suffix
# - Load the HDF5 file into a 2nd Keras model
# - Collect predictions from the 2nd model
# - Connect to postgres db with sqlalchemy
# - Save the HDF5 file as a BYTEA data type in a postgres row
# - Select the HDF5 file out of postgres into a new keras model
# - Use the new keras model to generate predictions

~/anaconda3/bin/python py/demokeras.py

exit

# I ran the above script and saw this:

dan@tkrapi:~/tkrapi20 $ demo/demo_keras.bash
Using TensorFlow backend.
x_a:
[[ 1.1  2.2]
 [ 2.1  3.2]
 [ 3.1  4.2]
 [ 4.1  5.2]
 [ 5.1  6.2]]
(5, 2)
y_a:
[[ 1.3]
 [ 2.1]
 [ 3.4]
 [ 4. ]
 [ 5.2]]
(5, 1)
Epoch 1/128
2017-11-17 17:52:19.660687: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasnt compiled to use ......
2017-11-17 17:52:19.660738: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasnt compiled to use ......
2017-11-17 17:52:19.660761: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasnt compiled to use ......
5/5 [==============================] - 0s - loss: 4.5122     
Epoch 2/128
5/5 [==============================] - 0s - loss: 4.2766     
Epoch 3/128
5/5 [==============================] - 0s - loss: 4.0298     
Epoch 4/128
5/5 [==============================] - 0s - loss: 3.8581     
Epoch 5/128

SNIP...

Epoch 125/128
5/5 [==============================] - 0s - loss: 0.1551     
Epoch 126/128
5/5 [==============================] - 0s - loss: 0.1549     
Epoch 127/128
5/5 [==============================] - 0s - loss: 0.1543     
Epoch 128/128
5/5 [==============================] - 0s - loss: 0.1541     
prediction_a:
[[ 2.91106105]]
prediction2_a:
[[ 2.91106105]]
prediction3_a:
[[ 2.91106105]]
dan@tkrapi:~/tkrapi20 $ 
