# 71: Find the shortest word(s) where some letter occurs 4 times.
# 72: Find the shortest word(s) where each vowel appears at least once.
# 73: Find the longest word(s) containing exactly 5 vowels.
# 74: Find the longest word(s) where the first three letters form a palindrome with the final three letters.
# 75: Find the longest word(s) with the longest contiguous block of a single letter (eg. three o's in a row).
# 76: Find the longest word(s) with the greatest number of a repeated letter.
# 77: Find the longest word(s) with the most number of adjacent pairs of identical letters (eg. buffoon but not banana).
# 78: (Ignored) Find the longest word(s) where each letter is repeated at least once.
# 79: (Ignored) Find the longest word(s) where each letter is repeated exactly one time.
# 80: Find the longest word(s) where no letter is repeated more than once.


import sys
idx = int(sys.argv[1]) - 71
myRegexLst = [
    r"/^(?=(\w)+(\w*\1){3}).{,6}$/im",
    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u).{,7}$/im",
    r"/^(?=(((?![aeiou].)*)[aeiou]((?![aeiou]).)*){5}$).{18,}$/im",
    r"/^(?=(.)(.)(.).*\3\2\1$).{13,}$/im",
    r"/^(?=.*(.)\1).{22,}$/im",
    r"/^(?=(.)+(.*\1){5,})\w*$/m",
    r"/(?=(.*(.)\2){3,})\w{14,}/m",
    r"//",
    r"//",
    r"/^(?!(.)+(.*\1){2,})\w{18,}$/im"
]
print(myRegexLst[idx])
