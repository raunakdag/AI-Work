import ast
import math
import sys
import matplotlib.pyplot as plt
import time

learning_rate = 1
epoch_amount = 100



def truth_table(bits, n):
    binary = bin(n)[2:]
    binary = ''.join('0' for x in range(pow(2, bits) - len(binary))) + binary

    tt = truthtable_helper(bits)
    new_tt_list = []

    for item in tt:
        temp_tuple = (tuple(item), int(binary[0:1]))
        new_tt_list.append(temp_tuple)
        binary = binary[1:]

    return tuple(new_tt_list)


def truthtable_helper(n):
    if n < 1:
        return [[]]
    subtable = truthtable_helper(n-1)
    return [row + [v] for row in subtable for v in [1,0]]


def pretty_print_tt(table):
    num_in_rows = len(table[0][0])
    str_p = '  ' + ''.join(f'{x+1}  ' for x in range(num_in_rows)) + '|  O\n'
    str_p += '----------------------\n'
    for a in table:
        str_p += '  ' + '  '.join([str(x) for x in a[0]]) + '  |  '  + str(a[1]) + '\n'
    return(str_p)


def perceptron(A, w, b, x):
    return A(float(dot(w, x)) + b)

def dot(x, y):
    return sum(x_i * y_i for x_i, y_i in zip(x, y))

def step(num):
    return 1 if num > 0 else 0

def update_weight(actual_output, current_weight, p_output, input_vector):
    # w = w + (f(x) - f*) * h * x
    to_mult = int((int(actual_output) - int(p_output)) * learning_rate)
    # print(input_vector)
    new_weight = tuple([to_mult * x for x in input_vector])
    return tuple(map(sum, zip(current_weight, new_weight)))

def update_bias(actual_output, current_bias, p_output):
    return float(current_bias) + float(int(actual_output) - int(p_output)) * float(learning_rate)

def check(n, w, b):
    bits = len(w)
    tt = truth_table(bits, n)
    amt_acct = 0
    for row in tt:
        if int(perceptron(step, w, b, row[0])) == int(row[1]):
            amt_acct += 1
    print(amt_acct/len(tt))


def test(num_bits, canonical):
    amt_accurate = 0
    current_tt = truth_table(num_bits, canonical)

    old_bias, old_weight = 0, tuple(0 for x in range(num_bits))
    for i in range(epoch_amount):
        new_bias, new_weight = old_bias, old_weight

        for row in current_tt:
            p_output = perceptron(step, new_weight, new_bias, row[0])
            new_bias = update_bias(row[1], new_bias, p_output)
            new_weight = update_weight(row[1], new_weight, p_output, row[0])

        if new_bias == old_bias and new_weight == old_weight:

            break

        old_bias, old_weight = new_bias, new_weight

    return(old_bias, old_weight)
    # print("Weight Vector: " + str(old_weight))
    # print("Bias Value: " + str(old_bias))
    # print(amt_accurate)
    # print(pow(2, pow(2, bits)))
    amt_accurate_in_perceptron = 0
    for row in current_tt:
        if perceptron(step, new_weight, new_bias, row[0]) == row[1]:
            amt_accurate_in_perceptron += 1

    # print("Accuracy: " + str(amt_accurate_in_perceptron/len(current_tt)))
    # print("Accuracy: " + str(amt_accurate/pow(2, pow(2, num_bits))))


# All bias/weight values below
# XOR HAPPENS HERE
def xor(x):
    w13 = 10
    w23 = 10
    b3 = -5
    w14 = -10
    w24 = -10
    b4 = 15
    w35 = 10
    w45 = 10
    b5 = -15

    # The three perceptron calls
    first_layer = perceptron(step, tuple([w13, w23]), b3, x)
    second_layer = perceptron(step, tuple([w14, w24]), b4, x)
    third_layer = perceptron(step, tuple([w35, w45]), b5, tuple([first_layer, second_layer]))

    return(third_layer)


def main():
    if len(sys.argv) == 2:
        input1 = str(sys.argv[1][1])
        input2 = str(sys.argv[1][4])
        x = [int(input1), int(input2)]
        print("XOR Result: " + str(xor(tuple(x))))
    elif len(sys.argv) == 3:
        num_bits = int(sys.argv[1])
        canonical = int(sys.argv[2])
        test(num_bits, canonical)

def ow():
    num_bits = 2
    canonical_weights = []
    canonical_bias = []


    for i in range(16):
        bias, weight = test(num_bits, i)
        canonical_weights.append(weight)
        canonical_bias.append(bias)
        # print(bias)
        # print(weight)

    # print(canonical_weights)
    # print(canonical_bias)
    x_coords = [-2.0 + 0.1 * float(x) for x in range(40)]
    y_coords = [-2.0 + 0.1 * float(x) for x in range(40)]

    # print(x_coords)

    for i in range(16):
        plt.axis([-2, 2, -2, 2])
        current_tt = truth_table(num_bits, i)
        # print(current_tt)
        for x in x_coords:
            for y in y_coords:
                if float(float(canonical_weights[i][0]) * x + float(canonical_weights[i][1]) * y) > -1 * canonical_bias[i]:
                    plt.scatter(x, y, s = 10, c = "green")
                else:
                    plt.scatter(x, y, s = 10, c = "red")
                for j in current_tt:
                    if j[1] == 1:
                        plt.scatter(j[0][0], j[0][1], s=50, c="green")
                    else:
                        plt.scatter(j[0][0], j[0][1], s=50, c="red")
        plt.show()
        time.sleep(10)
        plt.close()

ow()
