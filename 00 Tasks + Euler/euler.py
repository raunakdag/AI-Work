'''
Raunak Daga | Mr. Eckel PD 5 AI
'''
import random
# 0) The Benefits of Debugging
# 1) How to Open Debugger
# 2) How to Use Breakpoints
# 3) How to Find Values of Your Variables
# 4) How to Step Into/Out of Code
# 5) How to Use Console
# 6) How to Evaluate Expression
# 7) Useful Terms

def is_prime(x):
    if x == 1:
        return False

    if x == 2:
        return True
    else:
        for factor in range(2, x):
            if x % factor == 0:
                return False
        return True

max = 0
x = random.random()
for i in range(2, int(600851475143**(0.5))):
    if (600851475143 % i == 0):
        if(is_prime(i)):
            max = i


array = []
for i in range(10):
    print(is_prime(i))

# exit()
# break
# pass
# continue



# Problem 4
max = 0
for i in range(999):
    for j in range(999):
        if(i * j > max):
            if(str(i * j) == (str(i * j))[::-1]):
                max = i * j

print(max)

# Problem 7
numprimes = 0
numon = 1
while numprimes != 10001:
    if is_prime(numon):
        numprimes += 1
    # print(numon)
    if numprimes != 10001:
        numon += 1

print(numon)

# Problem 8
number = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"

max = 0

for i in range(987):
    cut = number[i: i + 13]
    num = 1
    for char in cut:
        num *= int(char)
    if num > max:
        max = num

print(max)

# Problem 9

to_do = True
for a in range(1, 500):
    for b in range(1, 500):
        c = 1000 - a - b
        if a**2 + b**2 == c**2:
            print(a * b * c)
            quit()
