import math
import numpy as np
import random

mock_run = True
weights = []
bias = []
network_size = [784, 300, 100, 10]

def sigmoid_step(num): return (1.0 / (1.0 + math.exp(-1.0 * num)))

def sigmoid_derivative(num): return float((1.0 / (1.0 + math.exp(-1.0 * num))) * (1.0 - (1.0 / (1.0 + math.exp(-1.0 * num)))))

def int_array(n):
    array = np.array([0 for x in range (10)])
    array[n] = 1
    return array.reshape(1, -1)

def get_data(file_name):
    data_set = []
    with open(file_name) as file:
        for line in file:
            row = line.strip().split(',')
            x_new = [float(a) / 255.0 for a in row[1: ]]
            data_set.append((np.asarray(x_new), int_array(int(row[0]))))
    return data_set

def backprop():
    data = get_data("mnist_train.csv")

    num_epoch = 0
    if mock_run:
        num_epoch = 3
    else:
        num_epoch = 100

    learning = 0.1
    weights = [None, np.random.rand(network_size[0], network_size[1]) * 2 - 1, np.random.rand(network_size[1], network_size[2]) * 2 - 1,
               np.random.rand(network_size[2], network_size[3]) * 2 - 1]
    bias = [None, np.random.rand(1, network_size[1]) * 2 - 1, np.random.rand(1, network_size[2]) * 2 - 1,
               np.random.rand(1, network_size[3]) * 2 - 1]

    sigmoid_vectorized = np.vectorize(sigmoid_step)
    sigmoid_derivative_vectorized = np.vectorize(sigmoid_derivative)

    for epoch in range(num_epoch):
        for x, y in data:
            dot_backprops = [0 for i in range(5)]
            a_backprops = [np.array([x]) for i in range (5)]
            delta_backprops = [np.zeros((1, 784)) for k in range(5)]

            for i in range(1, 4):
                dot_backprops[i] = (a_backprops[i - 1] @ weights[i]) + bias[i]
                a_backprops[i] = sigmoid_vectorized(dot_backprops[i])

            for i in range(3, 4):
                delta_backprops[i] = sigmoid_derivative_vectorized(dot_backprops[i]) * (y -a_backprops[i])

            for a in range(2, -1, -1):
                delta_backprops[a] = sigmoid_derivative_vectorized(dot_backprops[a]) * (delta_backprops[a + 1] @ weights[a + 1].transpose())

            for h in range(3, 0,-1):
                bias[h] = bias[h] + learning * delta_backprops[h]
                weights[h] = weights[h] + learning * (a_backprops[h - 1].transpose() @ delta_backprops[h])
        print("Epoch: " + str(epoch))
    return weights, bias

def p_net(dataset, weights, biases):
    print("Network: " + str(network_size))
    weights = weights [1: ]
    biases = biases [1: ]
    sigmoid_vectorized = np.vectorize(sigmoid_step)
    amt_wrong = 0
    for x_new, y in dataset:
        for i in range (3):
            x_new = sigmoid_vectorized(x_new @ weights[i] + biases[i])
        if x_new.argmax() != y.argmax():
            amt_wrong += 1
    print("Incorrect classifications: " + str(amt_wrong))
    print(float(amt_wrong) / len(dataset))

def main():
    test_set = get_data("mnist_test.csv")
    final_weights, final_biases = backprop()
    p_net(test_set, final_weights, final_biases)

main()
