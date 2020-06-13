import numpy as np
def der_A(x, y):
    return 8*x - 3*y + 24

def der_B(x, y):
    return -3*x + 4*y - 20

l = 0.2
loc = np.array([0.0, 0.0])
v = float('inf')
while not np.linalg.norm(v) < 10**-8:
    v = np.array([der_A(loc[0], loc[1]), der_B(loc[0], loc[1])])
    loc += -l*v
    print(loc, np.linalg.norm(v))