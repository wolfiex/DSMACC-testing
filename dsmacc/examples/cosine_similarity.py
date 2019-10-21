import tensorflow as tf
import numpy as np

def compute_cosine_distances(a, b):
    # x shape is n_a * dim
    # y shape is n_b * dim
    # results shape is n_a * n_b

    normalize_a = tf.nn.l2_normalize(a,1)
    normalize_b = tf.nn.l2_normalize(b,1)
    distance = 1 - tf.matmul(normalize_a, normalize_b, transpose_b=True)
    return distance

input_matrix = np.array([[1, 1, 1],
                         [0, 2, 1],
                         [0, 0, 1],
                         [0, 0, 1]], dtype = 'float32')

a = np.array([[2, 0, 1, 1, 0, 2, 1, 1],[2, 0, 1, 1, 0, 2, 1, 1],[2, 0, 1, 1, 0, 2, 1, 1]], dtype = 'float32')
b = np.array([[2, 0, 1, 1, 0, 1, 1, 1],[9, 0, 1, 1, 0, 2, 1, 1],[2, 0, 1, 1, 0, 2, 1, 1]], dtype = 'float32')

a = b = input_matrix


a = np.array([[2, 0, 1, 1, 0, 2, 1, 1]], dtype = 'float32')
b = np.array([[2, 0, 1, 1, 0, 3, 1, 1]], dtype = 'float32')


with tf.Session() as sess:
    e = sess.run(compute_cosine_distances(a,b))


print e
print ''

from sklearn.metrics.pairwise import cosine_distances
print(cosine_distances(a,b))



def compute_cosine_distances(a, b):
    # x shape is n_a * dim
    # y shape is n_b * dim
    # results shape is n_a * n_b

    normalize_a = tf.nn.l2_normalize(a,1)
    normalize_b = tf.nn.l2_normalize(b,1)
    distance = 1 - tf.matmul(normalize_a, normalize_b, transpose_b=True)
    return distance

a = np.array([[2, 0, 1]], dtype = 'float32')
b = np.array([[1, 0, 8]], dtype = 'float32')

with tf.Session() as sess:
    e = sess.run(compute_cosine_distances(tf.convert_to_tensor(a),tf.convert_to_tensor(b)))
    print e



a = np.array([[.2, 0, .1]], dtype = 'float32')
b = np.array([[.1, 0, .1]], dtype = 'float32')
with tf.Session() as sess:
    e = sess.run(compute_cosine_distances(tf.convert_to_tensor(a),tf.convert_to_tensor(b)))
    print e




print 'fi'
