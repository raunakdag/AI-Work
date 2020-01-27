from math import pi, acos, sin, cos
import os
import sys
import time
import heapq
from heapq import heappush, heappop

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('rrNodeCity.txt') as file:
    for line in file.readlines():
        line = line.replace("\n", "")
        print("\"" + line[line.find(" ") + 1:] + "\"" + ",")
