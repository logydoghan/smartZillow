import numpy as np
import pandas
import tensorflow as tf

# Feature, Label, Column
COLUMNS = ['zipcode', 'longitude', 'latitude', 'is_for_sale', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price']
CATEGORICAL_COLUMNS = ['zipcode', 'property_type']
CONTINUOUS_COLUMNS = ['bedroom', 'bathroom', 'size']
LABEL_COLUMN = 'list_price'
FEATURE_COLUMNS = ['zipcode', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price']


# input_fn return format: (feature_columns, label)
# feature_columns: {column_name : tf.constant}
# label: tf.constant
def input_fn(df):
    continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
    categorical_cols = {k: tf.SparseTensor(
        indices=[[i, 0] for i in range(df[k].size)],
        values=df[k].values,
        shape=[df[k].size, 1])
            for k in CATEGORICAL_COLUMNS}
    feature_columns = dict(continuous_cols.items() + categorical_cols.items())
    label = tf.constant(df[LABEL_COLUMN].values)
    return feature_columns, label


# Hanlding columns
zipcode = tf.contrib.layers.sparse_column_with_hash_bucket("zipcode", hash_bucket_size=1000)
property_type = tf.contrib.layers.sparse_column_with_hash_bucket("property_type", hash_bucket_size=100)
bedroom = tf.contrib.layers.real_valued_column("bedroom")
bathroom = tf.contrib.layers.real_valued_column("bathroom")
size = tf.contrib.layers.real_valued_column("size")
size_buckets = tf.contrib.layers.bucketized_column(size, boundaries=np.arange(6000, step=200).tolist())

feature_columns = [zipcode, property_type, bedroom, bathroom, size_buckets]

