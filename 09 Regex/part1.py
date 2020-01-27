# 30: Determine whether a string is either 0, 100, or 101.
# 31: Determine whether a given string is a binary string (ie. composed only of  0 and 1 characters).
# 32: Given a binary integer string, what regular expression determines whether it is even?
# 33: What is a regular expression to determine (ie. match) those words in a text that have at least two vowels?
# 34: Given a string, determine whether it is a non-negative, even binary integer string.
# 35: Determine whether a given string is a binary string containing 110 as a substring.
# 36: Match on all strings of length at least two, but at most four.
# 37: Validate a social security number entered into a field (ie. recognize ddd-dd-dddd where the d represents digits and where the dash indicates an arbitrary number of spaces with at most one dash).  For example, 542786363,   542  786363, and 542 – 78-6263 are all considered valid.
# 38: Determine a regular expression to help you find the first word of each line of text with a  d  in it: Match through the end of the first word with a d on each line that has a d.
# 39: Determine whether a string is a binary string that has the same number of 01 substrings as 10 substrings.

import sys
idx = int(sys.argv[1]) - 30
myRegexLst = [r"/^0$|^10[01]$/",  # 12 ^0$|
              r"/^[01]*$/",  # 7
              r"/0$/",  # 8
              r"/\w*[aeiou]\w*[aeiou]\w*/i",  # 23
              r"/^1[01]*0$|^0$/",  # 13
              r"/^[01]*110[01]*$/",  # 15
              r"/^.{2,4}$/s",  # 8
              r"/^\d{3} *-? *\d\d *-? *\d{4}$/",  # 28
              r"/^.*?d\w*/mi",  # 13
              r"/^0[01]*0$|^1[01]*?1$|^[01]?$/"
              ]
print(myRegexLst[idx])
