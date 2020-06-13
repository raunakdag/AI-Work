import sys


def gradientA(vector):
    x = float(vector[0])
    y = float(vector[1])
    return (float((8*x)-(3*y)+24), float(-3*x+4*y-20))


def gradientB(vector):
    x = vector[0]
    y = vector[1]
    return (float(2*x-(2*y**2)), float((4*y)*((-1*x)+y**2)+2*y-2))

def magnitude(vector):
    x = vector[0]
    y = vector[1]
    return (float(x * 2) + float(y**2)) * 0.5

def findLocalMin(vector,funct_name):
    curr_pos = vector
    while magnitude(funct_name(curr_pos)) > (10**(-8)):
        print("Current Position: ", curr_pos)
        gradient = funct_name(curr_pos)
        print("Gradient: ", gradient)
        lrGradient = tuple([LEARNING_RATE*i for i in gradient])
        curr_pos = tuple([curr_pos[i] - lrGradient[i] for i in range (len(lrGradient))])
        print()
    return curr_pos

functionName = "A"
LEARNING_RATE = 0.05
if functionName == "A":
    print(findLocalMin((0, 0), gradientA))
elif functionName == "B":
    print(findLocalMin((0, 0), gradientB))
