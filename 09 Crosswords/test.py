import re


def heuristic(puzzle):
    i = 3
    while True:
        # string_horizontal = r'(#?)' + r'-{3, }' + r'\1'
        string_horizontal = r'-' * i

        horizontal_matches = []
        match_on = re.search(string_horizontal, puzzle)
        horizontal_matches.append(match_on)
        if match_on:
            horizontal_matches.append(match_on)
            match_on = re.search(string_horizontal, puzzle,
                                 pos=horizontal_matches[-1].start() + 1)

        print(horizontal_matches)

        width = 6
        string_vertical = r'#' + \
            r'[-#\w]' * (width - 1) + (r'-' + (r'[-#\w]' *
                                               (width - 1))) * i + r'[-#\w]' + r'#'

        regex_match = re.search(string_vertical, puzzle)
        if regex_match:
            return regex_match.span()

        i += 1

def print_puzzle(puzzle):
    global height, width
    height = 9
    width = 4
    count = 0
    for i in range(len(puzzle)):
        if count != width - 1:
            print(puzzle[i], end='')
            count += 1
        else:
            print(puzzle[i])
            count = 0
    print()

def transpose(puzzle):
    global width
    width = 2
    new_puzzle = ''
    count = 0
    for i in range(len(puzzle)):
        if count != width - 1:
            new_puzzle += puzzle[i]
            count += 1
        else:
            new_puzzle += puzzle[i] + "\n"
            count = 0

    new_puzzle = ''.join([''.join(i) for i in zip(*new_puzzle.split())])
    return new_puzzle


string = '#---#I-----####-----n-----####-----c-----####-----l-----####-----e---------####-m---------####-e---------####-n---------####-t---------'
print_puzzle(string)

print_puzzle(transpose('12345678'))
# print(heuristic(string))

# print([''.join(i) for i in zip(*'12\n34\n56\n78'.split())])
