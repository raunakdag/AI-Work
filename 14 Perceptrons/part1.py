import ast
import math
import sys

def perceptron(A, w, b, x):
    return A(float(dot(w, x)) + b)

def dot(x, y):
    return sum(x_i * y_i for x_i, y_i in zip(x, y))

def step(num):
    return 1 if num > 0 else 0

def truth_table(bits, n):
    binary = bin(n)[2:]
    binary = ''.join('0' for x in range(pow(2, bits) - len(binary))) + binary

    tt = truthtable_helper(bits)
    new_tt_list = []

    for item in tt:
        temp_tuple = (tuple(item), binary[0:1])
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

def check(n, w, b):
    bits = len(w)
    tt = truth_table(bits, n)
    amt_acct = 0
    for row in tt:
        # print(perceptron(step, w, b, row[0]))
        # print(row[1])
        if int(perceptron(step, w, b, row[0])) == int(row[1]):
            amt_acct += 1
    print(amt_acct/len(tt))


# check(24, (1, 1, 0), 1)
check(int(sys.argv[1]), ast.literal_eval(sys.argv[2]), (float(sys.argv[3])))
