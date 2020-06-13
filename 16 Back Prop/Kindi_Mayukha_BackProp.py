# Mayukha Kindi
# 5/5/20
# Back Propagation

#---------------------------
#FORWARD PROPAGATION
import numpy as np
import math
import sys
import random
import os

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sigmoid(num):
    return float(1)/(1 + math.exp(-num))
sigmoid_ = np.vectorize(sigmoid)

w1_forward_prop = np.array([[1,-.5],[1,.5]])
b1_forward_prop = np.array([[1,-1]])
w2_forward_prop = np.array([[1,2],[-1,-2]])
b2_forward_prop = np.array([[-.5, .5]])
y = np.array([.8, 1])

def applyLayer(input, weights,biases,perceptron_func):
    dotProduct = (input@weights) + biases
    sigmoid_dotProduct = sigmoid_(dotProduct)
    return sigmoid_dotProduct

def forward_prop_error(predicted,actual):
    differences = tuple([float(float(predicted[i]) - float(actual[0][i]))**2 for i in range(len(predicted))])
    return float(0.5) * (differences[0] + differences[1])

WEIGHTS_FORWARD_PROP = [w1_forward_prop,w2_forward_prop]
BIAS_FORWARD_PROP = [b1_forward_prop, b2_forward_prop]
input = np.array([2, 3])
for i in range (0,2):
    input = applyLayer(input,WEIGHTS_FORWARD_PROP[i],BIAS_FORWARD_PROP[i],sigmoid_)
# print(forward_prop_error(y, input))

#----------------------
#HARDCODED BACK PROPOGATION TEST
def sigmoid_derivative(num):
    x = float((1)/(1 + math.exp(-num)))
    return float(x * (1.0-x))
sigmoid_derivative_ = np.vectorize(sigmoid_derivative)

LEARNING_RATE = 0.1
w1_forward_prop = np.array([[1,-.5],[1,.5]])
b1_forward_prop = np.array([[1,-1]])
w2_forward_prop = np.array([[1,2],[-1,-2]])
b2_forward_prop = np.array([[-.5, .5]])

WEIGHTS_FORWARD_PROP = [None,w1_forward_prop,w2_forward_prop]
BIAS_FORWARD_PROP = [None,b1_forward_prop, b2_forward_prop]

y = np.array([.8, 1])

inputs = [np.array([[2,3]])]
a_values = [0 for i in range (8)]
dot = [0 for i in range (8)]
delta = [np.array([[0,0]]) for n in range (8)]
for i in range(0,1):
    a_values[0] = inputs[-1]
    for layer in range(1,3):
        dot[layer] = (a_values[layer-1]@WEIGHTS_FORWARD_PROP[layer]) + BIAS_FORWARD_PROP[layer]
        a_values[layer] = sigmoid_(dot[layer])
    delta[2] = (sigmoid_derivative_(dot[2])) * (y - a_values[2])
    for k in range (1,-1,-1):
        delta[k] = sigmoid_derivative_(dot[k]) * (delta[k + 1] @ WEIGHTS_FORWARD_PROP[k + 1].T)
    for m in range (2,0,-1):
        BIAS_FORWARD_PROP[m] = BIAS_FORWARD_PROP[m] + LEARNING_RATE * delta[m]
        WEIGHTS_FORWARD_PROP[m] = WEIGHTS_FORWARD_PROP[m] + LEARNING_RATE * (a_values[m-1].T @ delta[m])

input1 = np.array([[2, 3]])
WEIGHTS_FORWARD_PROP_1 = [WEIGHTS_FORWARD_PROP[arr] for arr in range (1,3)]
BIAS_FORWARD_PROP_1 = [BIAS_FORWARD_PROP[arr] for arr in range(1,3)]
for i in range (0,2):
    input1 = applyLayer(input1,WEIGHTS_FORWARD_PROP_1[i],BIAS_FORWARD_PROP_1[i],sigmoid_)
# print(forward_prop_error(y, input1))


def main():
    network = sys.argv[1]
    def round(num):
        if num >= 0.5:
            return 1
        elif num < 0.5:
            return 0

    round_ = np.vectorize(round)
    if network == "S":
        def forward_prop_error_SUM(predicted,actual):
            return 0.5 * (np.linalg.norm(predicted - actual) ** 2)

        inputs_sum = [
            (np.array([[0,0]]), np.array([[0,0]])),
            (np.array([[0,1]]), np.array([[0,1]])),
            (np.array([[1,0]]), np.array([[0,1]])),
            (np.array([[1,1]]), np.array([[1,0]])),
        ]

        ERRORS = []
        for LEARNING_RATE in range (400):

            w1_sum = np.array([[random.uniform(-1, 1),random.uniform(-1, 1)],[random.uniform(-1, 1),random.uniform(-1, 1)]])
            b1_sum = np.array([[random.uniform(-1, 1),random.uniform(-1, 1)]])
            w2_sum = np.array([[random.uniform(-1, 1),random.uniform(-1, 1)],[random.uniform(-1, 1),random.uniform(-1, 1)]])
            b2_sum = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])

            WEIGHTS_SUM = [None,w1_sum,w2_sum]
            BIAS_SUM = [None,b1_sum, b2_sum]
            LEARNING_RATE_ = 10**random.uniform(-4, 1) # random.uniform(10**(-4),10**(-2))
            a_values_sum = [0 for i in range (8)]
            dot_sum = [0 for i in range (8)]
            delta_sum = [np.array([[0,0]]) for n in range (8)]
            for epoch in range (0,200):
                for x,y in inputs_sum:
                    a_values_sum[0] = x

                    for layer in range(1,3):
                        dot_sum[layer] = (a_values_sum[layer-1]@WEIGHTS_SUM[layer]) + BIAS_SUM[layer]
                        a_values_sum[layer] = sigmoid_(dot_sum[layer])

                    delta_sum[2] = (sigmoid_derivative_(dot_sum[2])) * (y - a_values_sum[2])

                    for k in range (1,-1,-1):
                        delta_sum[k] = sigmoid_derivative_(dot_sum[k]) * (delta_sum[k + 1] @ WEIGHTS_SUM[k + 1].T)

                    for m in range (2,0,-1):
                        BIAS_SUM[m] = BIAS_SUM[m] + LEARNING_RATE_ * delta_sum[m]
                        WEIGHTS_SUM[m] = WEIGHTS_SUM[m] + LEARNING_RATE_ * (a_values_sum[m-1].T @ delta_sum[m])

            WEIGHTS_SUM = [WEIGHTS_SUM[arr] for arr in range (1,3)]
            BIAS_SUM = [BIAS_SUM[arr] for arr in range(1,3)]
            ind_error = 0.0

            for datapoint,correct_output in inputs_sum:
                ind_error = 0

                for i in range (0,2):
                    datapoint = applyLayer(datapoint,WEIGHTS_SUM[i],BIAS_SUM[i],sigmoid_)

                error = forward_prop_error_SUM(correct_output, datapoint)
                # print("Error: ", error)
                ind_error = ind_error + error

            ERRORS.append((ind_error,LEARNING_RATE, WEIGHTS_SUM,BIAS_SUM,LEARNING_RATE_))

        # print(min(ERRORS)[4]))
        for x in inputs_sum:
            print("Input: ", x[0])
            for i in range (0,2):
                w = (min(ERRORS))[2][i]
                b = min(ERRORS)[3][i]
                # print(w)
                # print(b)
                # print(ERRORS)
                # print(min(ERRORS))[2]
                # print(min(ERRORS))[3]
                x = applyLayer(x,w,b,sigmoid_)
            print("Unrounded Output: ", x[0])
    elif network == "C":
        LEARNING_RATE_C = 0.4

        def inside_or_outside_circle(x_, y_):
            if math.sqrt(x ** 2 + y ** 2) <= 1:
                return 1
            else:
                return 0

        def forward_prop_error_circle(predicted, actual):
            differences = tuple([float(float(predicted[0]) - float(actual[0])) ** 2])
            return float(0.5) * (differences[0])

        POINTS = []
        file = "10000_pairs.txt"
        with open(file) as f:
            for line in f:
                x, y = float(line.split(" ")[0]), float(line.split(" ")[1])
                result = inside_or_outside_circle(x, y)
                POINTS.append((np.array([[x, y]]), np.array([result])))
        WEIGHTS_CIRCLE = [None, np.array([[1, -1], [-1, -1], [1, 1], [-1, 1]]).T, np.array([[1, 2, 3, 4]]).T]
        BIAS_CIRCLE = [None, np.array([[1], [1], [1], [1]]).T, np.array([[-6.12]]).T]


        a_values_circle = [0 for i in range(3)]
        dot_circle = [0 for i in range(3)]
        delta_circle = [np.array([[0, 0]]) for n in range(8)]


        for epoch in range(0, 1):
            print("Epoch: ", epoch)
            for pt, classification in POINTS:
                a_values_circle[0] = pt

                for layer in range(1, 3):
                    print(dot_circle[layer])
                    print(a_values_circle[layer-1])
                    print(WEIGHTS_CIRCLE[layer])
                    print(BIAS_CIRCLE[layer])
                    dot_circle[layer] = (a_values_circle[layer - 1] @ WEIGHTS_CIRCLE[layer]) + BIAS_CIRCLE[layer]
                    print(sigmoid_(dot_circle[layer]))
                    a_values_circle[layer] = sigmoid_(dot_circle[layer])
                print()
                delta_circle[2] = (sigmoid_derivative_(dot_circle[2])) * (classification - a_values_circle[2])

                for k in range(1, -1, -1):
                    print(delta_circle[k])
                    print(dot_circle[k])
                    print()
                    delta_circle[k] = sigmoid_derivative_(dot_circle[k]) * (
                                delta_circle[k + 1] @ WEIGHTS_CIRCLE[k + 1].T)

                # exit()
                for m in range(2, 0, -1):
                    print("Check here")
                    print(BIAS_CIRCLE[m])
                    print(delta_circle[m])
                    print()
                    BIAS_CIRCLE[m] = BIAS_CIRCLE[m] + LEARNING_RATE_C * delta_circle[m]
                    print(BIAS_CIRCLE[m])
                    print(delta_circle[m])
                    WEIGHTS_CIRCLE[m] = WEIGHTS_CIRCLE[m] + LEARNING_RATE_C * (
                                a_values_circle[m - 1].T @ delta_circle[m])
                    print(WEIGHTS_CIRCLE[m])
                exit()
            WEIGHTS_CIRCLE_r = [WEIGHTS_CIRCLE[arr] for arr in range(1, 3)]
            BIAS_CIRCLE_r = [BIAS_CIRCLE[arr] for arr in range(1, 3)]
            misclassified = 0
            for datapoint, correct_output in POINTS:
                for i in range(0, 2):
                    datapoint = applyLayer(datapoint, WEIGHTS_CIRCLE_r[i], BIAS_CIRCLE_r[i], sigmoid_)
                print(datapoint[0])
                print(correct_output[0])
                if round(datapoint[0]) != correct_output[0]:
                    misclassified = misclassified + 1
            print("Misclassified number of points: ", misclassified)

main()
