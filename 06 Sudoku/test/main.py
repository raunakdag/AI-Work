import os
import math
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

count = 0
with open('output.txt') as file:
    for line in file:
        count += 1

print(count)
