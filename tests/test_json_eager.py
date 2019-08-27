# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
# ==============================================================================
"""Tests for JSON Dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf
if not (hasattr(tf, "version") and tf.version.VERSION.startswith("2.")):
  tf.compat.v1.enable_eager_execution()
import tensorflow_io as tfio  # pylint: disable=wrong-import-position
import tensorflow_io.json as json_io  # pylint: disable=wrong-import-position

def test_io_tensor_json_recods_mode():
  """Test case for tfio.IOTensor.from_json."""
  x_test = [[1.1, 2], [2.1, 3]]
  y_test = [[2.2, 3], [1.2, 3]]
  feature_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "feature.json")
  feature_filename = "file://" + feature_filename
  label_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "label.json")
  label_filename = "file://" + label_filename

  features = tfio.IOTensor.from_json(feature_filename, mode='records')
  assert features("floatfeature").dtype == tf.float64
  assert features("integerfeature").dtype == tf.int64

  labels = tfio.IOTensor.from_json(label_filename, mode='records')
  assert labels("floatlabel").dtype == tf.float64
  assert labels("integerlabel").dtype == tf.int64

  float_feature = features("floatfeature")
  integer_feature = features("integerfeature")
  float_label = labels("floatlabel")
  integer_label = labels("integerlabel")

  for i in range(2):
    v_x = x_test[i]
    v_y = y_test[i]
    assert v_x[0] == float_feature[i].numpy()
    assert v_x[1] == integer_feature[i].numpy()
    assert v_y[0] == float_label[i].numpy()
    assert v_y[1] == integer_label[i].numpy()

  feature_dataset = features.to_dataset()

  label_dataset = labels.to_dataset()

  dataset = tf.data.Dataset.zip((
      feature_dataset,
      label_dataset
  ))

  i = 0
  for (j_x, j_y) in dataset:
    v_x = x_test[i]
    v_y = y_test[i]
    for index, x in enumerate(j_x):
      assert v_x[index] == x.numpy()
    for index, y in enumerate(j_y):
      assert v_y[index] == y.numpy()
    i += 1
  assert i == len(y_test)

def test_io_tensor_json():
  """Test case for tfio.IOTensor.from_json."""
  x_test = [[1.1, 2], [2.1, 3]]
  y_test = [[2.2, 3], [1.2, 3]]
  feature_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "feature.ndjson")
  feature_filename = "file://" + feature_filename
  label_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "label.ndjson")
  label_filename = "file://" + label_filename

  features = tfio.IOTensor.from_json(feature_filename)
  assert features("floatfeature").dtype == tf.float64
  assert features("integerfeature").dtype == tf.int64

  labels = tfio.IOTensor.from_json(label_filename)
  assert labels("floatlabel").dtype == tf.float64
  assert labels("integerlabel").dtype == tf.int64

  float_feature = features("floatfeature")
  integer_feature = features("integerfeature")
  float_label = labels("floatlabel")
  integer_label = labels("integerlabel")

  for i in range(2):
    v_x = x_test[i]
    v_y = y_test[i]
    assert v_x[0] == float_feature[i].numpy()
    assert v_x[1] == integer_feature[i].numpy()
    assert v_y[0] == float_label[i].numpy()
    assert v_y[1] == integer_label[i].numpy()

  feature_dataset = features.to_dataset()

  label_dataset = labels.to_dataset()

  dataset = tf.data.Dataset.zip((
      feature_dataset,
      label_dataset
  ))

  i = 0
  for (j_x, j_y) in dataset:
    v_x = x_test[i]
    v_y = y_test[i]
    for index, x in enumerate(j_x):
      assert v_x[index] == x.numpy()
    for index, y in enumerate(j_y):
      assert v_y[index] == y.numpy()
    i += 1
  assert i == len(y_test)

def test_json_dataset():
  """Test case for JSON Dataset.
  """
  x_test = [[1.1, 2], [2.1, 3]]
  y_test = [[2.2, 3], [1.2, 3]]
  feature_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "feature.json")
  feature_filename = "file://" + feature_filename
  label_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "label.json")
  label_filename = "file://" + label_filename

  feature_cols = json_io.list_json_columns(feature_filename)
  assert feature_cols["floatfeature"].dtype == tf.float64
  assert feature_cols["integerfeature"].dtype == tf.int64

  label_cols = json_io.list_json_columns(label_filename)
  assert label_cols["floatlabel"].dtype == tf.float64
  assert label_cols["integerlabel"].dtype == tf.int64

  feature_dataset = json_io.JSONDataset(
      feature_filename, ["floatfeature", "integerfeature"]
  ).apply(tf.data.experimental.unbatch())

  label_dataset = json_io.JSONDataset(
      label_filename, ["floatlabel", "integerlabel"]
  ).apply(tf.data.experimental.unbatch())


  dataset = tf.data.Dataset.zip((
      feature_dataset,
      label_dataset
  ))

  i = 0
  for (j_x, j_y) in dataset:
    v_x = x_test[i]
    v_y = y_test[i]
    for index, x in enumerate(j_x):
      assert v_x[index] == x.numpy()
    for index, y in enumerate(j_y):
      assert v_y[index] == y.numpy()
    i += 1
  assert i == len(y_test)

def test_json_keras():
  """Test case for JSONDataset with keras."""
  feature_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "iris.json")
  feature_filename = "file://" + feature_filename
  label_filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "test_json",
      "species.json")
  label_filename = "file://" + label_filename

  feature_cols = ["sepalLength", "sepalWidth", "petalLength", "petalWidth"]
  label_cols = ["species"]

  feature_dataset = json_io.JSONDataset(feature_filename, feature_cols)

  label_dataset = json_io.JSONDataset(label_filename, label_cols)

  dataset = tf.data.Dataset.zip((
      feature_dataset,
      label_dataset
  ))
  def pack_features_vector(features, labels):
    """Pack the features into a single array."""
    features = tf.stack(list(features), axis=1)
    return features, labels
  dataset = dataset.map(pack_features_vector)

  model = tf.keras.Sequential([
      tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(4,)),  # input shape required
      tf.keras.layers.Dense(10, activation=tf.nn.relu),
      tf.keras.layers.Dense(3)
  ])

  model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
  model.fit(dataset, epochs=5)

if __name__ == "__main__":
  test.main()
