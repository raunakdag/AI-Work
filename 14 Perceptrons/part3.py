import sys
import numpy as np
import random
import math

def step(num): return 1 if num > 0 else 0

def diamond_step(num): return int(num > 0.0)

def sigmoid_step(num): return (1.0 / (1.0 + math.exp(-1.0 * num)))

def p_net(A, x):
    # XOR HAPPENS HERE
    weights = [np.array([[10, -10], [10, -10]]), np.array([[10], [10]])]
    biases = [np.array([[-5, 15]]), np.array([[-15]])]
    x = np.array([[x[0], x[1]]])

    a0 = x
    for i in range(0, 2):
        a0 = A(a0 @ weights[i] + biases[i])
    return a0[0][0]


def diamond(A, x):
    weights = [np.array([[1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, -1.0]]), np.array([[1.0], [1.0], [1.0], [1.0]])]
    biases = [np.array([[-1.0, -1.0, -1.0, -1.0]]), np.array([[0.0]])]
    x = np.array([[x[0], x[1]]])

    a0 = x
    for i in range(0, 2):
        a0 = A(a0 @ weights[i] + biases[i])
    return 'Inside' if str(a0[0][0]) == '0' else 'Outside'


def circle(A, x):
    weights = [np.array([[1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, -1.0]]), np.array([[1.0], [1.0], [1.0], [1.0]])]
    biases = [np.array([[-1.35, -1.35, -1.35, -1.35]]), np.array([[-1.0]])]
    x = np.array([[x[0], x[1]]])

    a0 = x
    for i in range(0, 2):
        a0 = A(a0 @ weights[i] + biases[i])
    # print(a0)
    return 'Inside' if str(int(round(a0[0][0]))) == '0' else 'Outside'

def main():
    if len(sys.argv) == 1:
        failed = []
        amt_accurate = 0
        for i in range(500):
            x = [random.random(), random.random()]
            A = np.vectorize(sigmoid_step)
            if circle(A, tuple(x)) == 'Inside' and math.sqrt(x[0]**2 + x[1]**2) <= 1 or circle(A, tuple(x)) == 'Outside' and math.sqrt(x[0]**2 + x[1]**2) > 1:
                amt_accurate += 1
            else:
                failed.append(x)

        print("Failed: " + str(failed))
        print("Percent accurate: " + str(amt_accurate/500))
    elif len(sys.argv) == 2:
        input1, input2 = str(sys.argv[1][1]), str(sys.argv[1][4])
        x = [int(input1), int(input2)]
        A = np.vectorize(step)
        print("XOR Result: " + str(p_net(A, tuple(x)))) # XOR HAPPENS HERE
    elif len(sys.argv) == 3:
        input1, input2 = sys.argv[1], sys.argv[2]
        x = [float(input1), float(input2)]
        A = np.vectorize(diamond_step)
        print("Diamond Result: " + str(diamond(A, tuple(x))))

main()
