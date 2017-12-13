# Feel free to add any functions, import statements, and variables.
import numpy as np
import pandas as pd
import tensorflow as tf


def predict(file):
    # Fill in this function. This function should return a list of length 52
    #   which is filled with floating point numbers. For example, the current
    #   implementation predicts all the instances in test.csv as 10.0.

    # 10 years data
    data = pd.read_csv('train.csv')
    train_data = data.set_index("Date")

    # 10 years data for training
    train_X = train_data.iloc[:, :6].as_matrix()
    train_Y = train_data.iloc[:, 6:].as_matrix()

    #model
    timesteps = 6
    data_dim = 1
    output_dim = 1
    learning_rate = 0.001
    training_epoch = 1000

    X = tf.placeholder(tf.float32, [None, timesteps, data_dim])
    Y = tf.placeholder(tf.float32, [None, output_dim])

    cells = []
    for num in range(3):
        # num_units을 크게 주면 epoch이 400을 넘어가며 널뛰기하는 현상보임. 128이하가 적당한 것을 발견
        cell = tf.contrib.rnn.BasicLSTMCell(num_units=256, state_is_tuple=True)
        # cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob = 0.7)
        cells.append(cell)

    cell = tf.contrib.rnn.MultiRNNCell(cells)
    outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    Y_pred = tf.contrib.layers.fully_connected(outputs[:, -1], output_dim, activation_fn=None)
    loss = tf.reduce_mean(tf.square(Y_pred - Y))

    learning_rate = 0.005
    optimizer = tf.train.AdamOptimizer(learning_rate)
    train = optimizer.minimize(loss)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    reshaped_train_X = train_X.reshape((*train_X.shape, 1))

    for epoch in range(training_epoch):
        _, l = sess.run([train, loss], feed_dict={X: reshaped_train_X, Y: train_Y})

    # Test step
    test_data = pd.read_csv(file)
    test_data = test_data.set_index("Date")
    test_X = test_data.iloc[:, :6].as_matrix()
    reshaped_test_X = test_X.reshape((*test_X.shape, 1))

    test_predict = sess.run(Y_pred, feed_dict={X: reshaped_test_X})
    result = [i[0] for i in test_predict]

    return result


def write_result(predictions):
    # You don't need to modify this function.
    with open('result.csv', 'w') as f:
        f.write('Value\n')
        for l in predictions:
            f.write('{}\n'.format(l))


def main():
    # You don't need to modify this function.
    predictions = predict('test.csv')
    write_result(predictions)


if __name__ == '__main__':
    # You don't need to modify this part.
    main()
