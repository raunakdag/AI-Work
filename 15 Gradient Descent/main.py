import numpy as np
import sys
import math

learn = .1

def A(x, y):
    return [x * 8.0 - 3.0 * y + 24.0, x * -3.0 + y * 4.0 - 20.0]

def B(x, y):
    return (2.0 * x - 2 * math.pow(y, 2), 4 * y * (-x + math.pow(y, 2)) + 2 * y - 2.0)


def main():
    if sys.argv[1] == "A":
        vector = np.array([0.0, 0.0])
        magnitude = 100000.0
        while np.linalg.norm(magnitude) > (math.pow(10, -8)):
            magnitude = np.array(A(vector[0], vector[1]))
            total_rate = learn * magnitude
            vector -= total_rate
            print(str(vector) + " " + str(np.linalg.norm(magnitude)))
        print(vector)
    elif sys.argv[1] == "B":
        vector = np.array([0.0, 0.0])
        magnitude = 100000.0
        while np.linalg.norm(magnitude) > (math.pow(10, -8)):
            magnitude = np.array(B(vector[0], vector[1]))
            total_rate = learn * magnitude
            vector -= total_rate
            print(str(vector) + " " + str(magnitude))
        print(vector)


main()
