import numpy as np
import math

w_0 = np.matrix([[-1, -.5], [1, .5]])
w_1 = np.matrix([[1, 2], [-1, -2]])
b_1 = np.matrix([[1, -1]])
b_2 = np.matrix([[-.5, .5]])
x = np.matrix([[2, 3]])
y = np.matrix([[.8, 1]])

sample_w = np.matrix([[0] * 2, [0] * 2])
sample_final_w = np.matrix([[0] * 4])
sample_b = np.matrix([[0] * 2])
n = 2
lmda = 0.1


def get_error(w0, w1, b1, b2, x_vec, y_vec):
    a0 = x_vec
    dot1 = a0 * w0 + b1
    a1 = sigmoid(dot1)
    dot2 = a1 * w1 + b2
    a2 = sigmoid(dot2)
    return 1/2 * np.linalg.norm(y_vec - a2) ** 2


def sigmoid_function(prod):
    k = -1
    return 1/(1 + math.e ** (k * prod))


def sigmoid_function_prime(prod):
    sgmd = sigmoid_function(prod)
    return sgmd * (1 - sgmd)


sigmoid = np.vectorize(sigmoid_function)
sigmoid_prime = np.vectorize(sigmoid_function_prime)


def back_propagation():
    err = float('inf')
    weight = [w_0, w_1]
    bias = [None, b_1, b_2]
    a = [np.matrix([[]])] * (n + 1)
    dot = [np.matrix([[]])] * (n + 1)
    delta = [np.matrix([[]])] * (n + 1)
    a[0] = x
    while err > 0:
        for l in range(1, n + 1):
            dot[l] = a[l - 1] * weight[l - 1] + bias[l]
            a[l] = sigmoid(dot[l])
        delta[n] = np.multiply(sigmoid_prime(dot[n]), (y - a[n]))
        for l in range(n - 1, 0, -1):
            delta[l] = np.multiply(sigmoid_prime(dot[l]), delta[l + 1] * np.transpose(weight[l]))
        for l in range(n):
            weight[l] = weight[l] + lmda * np.transpose(a[l]) * delta[l + 1]
            bias[l + 1] = bias[l + 1] + lmda * delta[l + 1]
        err = get_error(weight[0], weight[1], bias[1], bias[2], x, y)
        print(err)


print(get_error(w_0, w_1, b_1, b_2, x, y))
back_propagation()
