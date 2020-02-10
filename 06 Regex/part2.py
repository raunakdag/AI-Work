# Q40: Write a regular expression that will match on an Othello board represented as a string.
# Q41: Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
# Q42: Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole
# (assuming it could), it will be connected to one of the corners through X tokens.  Specifically, this means
# that one of the ends must be a hole, or starting from an end there is a sequence of at least one x followed
# immediately by a sequence (possibly empty) of o, immediately followed by a hole.
# Q43: Match on all strings of odd length.
# Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
# Q45: Match all words having two adjacent vowels that differ.
# Q46: Match on all binary strings which DON’T contain the substring 110.
# Q47: Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
# Q48: Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
# Q49: Match on all positive, even, base 3 integer strings

import sys
idx = int(sys.argv[1]) - 40
myRegexLst = [r"/^[ox.]{64}$/i",  # Shortest
              r"/^[ox]*\.[ox]*$/i",
              r"/^\.|\.$|^x+o*\.|\.o*x+$/i",  # /^(X+o*)?\.|\.(o*x+)?$/i
              r"/^.(..)*$/s",
              r"/^0([01]{2})*$|^1[01]([01]{2})*$/",
              r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
              r"/^(10|0)*1*$/",
              r"/^(a|[bc]+a?)[bc]*$/",  # /^[bc]*[abc][bc]*$/ # /^(b|c|a[bc]*$)+$/
              r"/^([bc]*a[bc]*a[bc]*)+$|^[bc]+$/",
              r"/^((2|1[20]*1)0*)+$/",  # 2 signifies an even base 3 number


              ]
print(myRegexLst[idx])
