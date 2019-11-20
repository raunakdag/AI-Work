import sys

# Question 1
# print(int(sys.argv[1]) + int(sys.argv[2]))
#
# Question 2
# listNums = sys.argv[1:]
# sum = 0
# for i in listNums:
#     sum = sum + int(i)
# print(sum)
#
# Question 3
# listNums = sys.argv[1:]
# sum = 0
# for i in listNums:
#     if int(i) % 3 == 0:
#         sum = sum + int(i)
#
# print(sum)
#
# Question 4
# n = 1
# lastN = 1
# for i in range(0, int(sys.argv[1])):
#     print(lastN)
#     n = n + lastN
#     lastN = n - lastN
#
# Question 5
# firstInt = int(sys.argv[1])
# secondInt = int(sys.argv[2])
#
# for i in range(firstInt, secondInt + 1):
#     print(pow(i, 2) - 3 * i + 2)
#
# Question 6
# firstSide = float(sys.argv[1])
# secondSide = float(sys.argv[2])
# thirdSide = float(sys.argv[3])
#
# sides = [firstSide, secondSide, thirdSide]
# sides = sorted(sides)
#
#
# if sides[0] + sides[1] < sides[2]:
#     print("Impossible triangle")
#     exit()
#
# halfPerim = sum(sides) / 2
# print(pow((halfPerim * (halfPerim - sides[0]) *
#            (halfPerim - sides[1]) * (halfPerim - sides[2])), 1 / 2.0))
#
# Question 7
# string = sys.argv[1]
# vowels = {
#     "a": 0,
#     "e": 0,
#     "i": 0,
#     "o": 0,
#     "u": 0
# }
#
# for i in string:
#     if i in vowels:
#         vowels[i] = vowels[i] + 1
#
# print(vowels)
#
# Question 8
#
# name = 'N/A'
#
# while name != 'quit':
#     name = input("Enter your name: ")
#     print(name)
#
# Question 9
#
# name = []
# inputWord = ''
#
# while inputWord != 'quit':
#     inputWord = str(input("Enter your name: "))
#     name.append(inputWord)
#     print(name)
#
# Question 10
# s = "\"Don't quote me,\" she said."
