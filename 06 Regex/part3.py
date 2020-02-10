# Q50: Match all words where some letter appears twice in the same word.
# Q51: Match all words where some letter appears four times in the same word.
# Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
# Q53: Match all six letter words containing the substring cat.
# Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
# Q55: Match all six letter words not containing the substring cat.
# Q56: Match all words with no repeated characters.
# Q57: Match all binary strings not containing the forbidden substring 10011.
# Q58: Match all words having two different adjacent vowels.
# Q59: Match all binary strings containing neither 101 nor 111 as substrings.

import sys
idx = int(sys.argv[1]) - 50
myRegexLst = [
    r"/\w*(\w)\w*(\1\w*)/i",
    r"/\w*(\w)\w*(\1\w*){3}/i",
    r"/^([10])([10]*\1)*$/",
    r"/\b(?=\w*cat\w*)\w{6}\b/i",
    r"/\b(?=\w*bri\w*)(?=\w*ing\w*)\w{5,9}\b/i",
    r"/\b(?!\w*cat\w*)\w{6}\b/i",
    r"/\b(?!\w*(\w)\w*\1\w*)\w+\b/i",
    r"/^(0|1(?!0011))*$/",
    r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
    r"/^(0|1(?!11)(?!01))*$/"
]
print(myRegexLst[idx])
