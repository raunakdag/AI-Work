import sys
import re
import random


# Sets up the initial puzzle for the rest of the game
def create_initial_puzzle(size):
    global height, width, len_p, num_blocked
    height, width = int(size.split('x')[0]), int(size.split('x')[1])
    len_p = height * width
    num_blocked = int(sys.argv[2])

    puzzle = '-' * len_p

    if num_blocked % 2 == 1:
        puzzle = place_at_index(puzzle, '#', len_p // 2)

    if num_blocked == len_p:
        puzzle = '#' * len_p

    # Iterating through each seedstring
    for arg_num in range(4, len(sys.argv)):
        seedstring = sys.argv[arg_num]
        direction = seedstring[0].upper()
        x, y = int(re.findall(r'\d+', seedstring)
                   [0]), int(re.findall(r'\d+', seedstring)[1])
        word = seedstring[seedstring.rfind(str(y)) + len(str(y)):]
        start_index = convert(x, y)

        if direction == 'V':
            for i in range(len(word)):
                if word[i] == '#':
                    puzzle = implied(puzzle, start_index + width * i)
                puzzle = place_at_index(
                    puzzle, word[i], start_index + width * i)
        elif direction == 'H':
            for i in range(len(word)):
                if word[i] == '#':
                    puzzle = implied(puzzle, start_index + i)
                puzzle = place_at_index(puzzle, word[i], start_index + i)

    return puzzle


def fix_invalid_islands(puzzle):
    indexes = []
    for i in range(len(puzzle)):
        if puzzle[i] == '-':
            indexes.append(i)

    for index in indexes:
        if implied(puzzle, index) is not None:
            if connected(implied(puzzle, index)):
                return implied(puzzle, index)

# ----------------- BUILDING PUZZLE METHODS -------------- #


# Checks if a puzzle has any nonconnected blocks. Uses area fill.
def connected(puzzle):
    global height, width, len_p

    for i in range(len_p):
        puzzle = place_at_index(puzzle, '?', i) if puzzle[i] != '#' else puzzle

    queue = [puzzle.find('?')] if '?' in puzzle else None
    h_dir, v_dir = [-1, 1], [-width, width]

    while queue:
        i = queue.pop(0)
        block_row = i // width
        if puzzle[i] != '!' and puzzle[i] != '#':
            puzzle = place_at_index(puzzle, '!', i)

            for dir in h_dir:
                if (i + dir) < len(puzzle) and (i + dir) >= 0 and puzzle[i + dir] == '?' and (i + dir) // width == block_row:
                    queue.append(i + dir)

            for dir in v_dir:
                if (i + dir) < len(puzzle) and (i + dir) >= 0 and puzzle[i + dir] == '?':
                    queue.append(i + dir)

    return False if '?' in puzzle else True


def implied(puzzle, index):
    global height, width, len_p

    if puzzle[index] == '#':
        return puzzle
    elif puzzle[index] != '-':
        return None

    to_be_implied = set()
    puzzle = place_at_index(puzzle, '#', index)

    if puzzle[opposite(index)] == '-':
        to_be_implied.add(opposite(index))

    block_row, block_col = index // width, index % width

    h_dir, v_dir = [-1, 1], [-width, width]

    for dir in h_dir:
        i, possible_implications = 1, []
        while (index + i * dir) >= 0 and (index + i * dir) < len_p and puzzle[index + i * dir] != '#' and i < 3:
            if (index + i * dir) // width == block_row:
                possible_implications.append(index + i * dir)
            i += 1

        if possible_implications:
            fpi = possible_implications[-1]
            if fpi + dir >= 0 and fpi + dir < len_p and puzzle[fpi + dir] == '#' and (fpi + dir) // width == block_row:
                for to_be_added in possible_implications:
                    to_be_implied.add(to_be_added)

    for dir in v_dir:
        i, possible_implications = 1, []
        while (index + i * dir) >= 0 and (index + i * dir) < len_p and puzzle[index + i * dir] != '#' and i < 3:
            possible_implications.append(index + i * dir)
            i += 1

        if possible_implications:
            fpi = possible_implications[-1]
            if fpi + dir >= 0 and fpi + dir < len_p and puzzle[fpi + dir] == '#':
                for to_be_added in possible_implications:
                    to_be_implied.add(to_be_added)

    # Checking if a blocking character is close to the edge left/right
    if block_col <= 2:
        if block_col == 1:
            to_be_implied.add(index - 1)
        if block_col == 2:
            to_be_implied.add(index - 2)
            to_be_implied.add(index - 1)

    if block_col >= (width - 3):
        if block_col == (width - 3):
            to_be_implied.add(index + 2)
            to_be_implied.add(index + 1)
        if block_col == (width - 2):
            to_be_implied.add(index + 1)

    # Checking if a blocking character is close to the north/south
    if block_row <= 2:
        if block_row == 1:
            to_be_implied.add(index - width)
        if block_row == 2:
            to_be_implied.add(index - width)
            to_be_implied.add(index - 2 * width)

    if block_row >= (height - 3):
        if block_row == (height - 3):
            to_be_implied.add(index + 2 * width)
            to_be_implied.add(index + width)
        if block_row == (height - 2):
            to_be_implied.add(index + width)

    for index_to_do in to_be_implied:
        if num_blocked % 2 == 0 and len_p // 2 == index_to_do and len_p % 2 == 1:
            return None
        if puzzle is not None:
            puzzle = implied(puzzle, index_to_do)

    return puzzle


def backtrack(puzzle):
    print_puzzle(puzzle)
    print(heuristic(puzzle))
    global height, width, num_blocked
    if not connected(puzzle) or puzzle.count('#') > num_blocked:
        return None
    if puzzle.count('#') == num_blocked:
        return puzzle

    possible_indexes = get_all_indexes(puzzle)
    random.shuffle(possible_indexes)
    for new_index in possible_indexes:
        new_puzzle = implied(puzzle, new_index)
        if new_puzzle is not None:
            backtracked_puzzle = backtrack(new_puzzle)
            if backtracked_puzzle is not None:
                return backtracked_puzzle

    return None


def get_all_indexes(puzzle):
    indexes = []
    for i in range(len(puzzle)):
        if puzzle[i] == '-' and puzzle[opposite(i)] == '-':
            if num_blocked % 2 == 0 and len_p // 2 == i:
                pass
            else:
                indexes.append(i)
    return indexes

def heuristic(puzzle):
    i = 3
    while True:
        string_horizontal = r'#' + r'-' * i + r'#'
        regex_match = re.search(string_horizontal, puzzle)
        if regex_match:
            return regex_match.span()

        width = 4
        string_vertical = r'#' + \
            r'[-#\w]' * (width - 1) + (r'-' + (r'[-#\w]' *
                                               (width - 1))) * i + r'[-#\w]' + r'#'
        print(string_vertical)
        regex_match = re.search(string_vertical, puzzle)
        if regex_match:
            return regex_match.span()

        i += 1


# ----------------------------- HELPER METHODS --------------------  #


def convert(x, y):
    global width
    return x * width + y

def opposite(index):
    global len_p
    return len_p - index - 1

def place_at_index(puzzle, char, index):
    return puzzle[0: (index)] + char + puzzle[(index) + 1:]

def print_puzzle(puzzle):
    global height, width
    count = 0
    for i in range(len(puzzle)):
        if count != width - 1:
            print(puzzle[i], end='')
            count += 1
        else:
            print(puzzle[i])
            count = 0
    print()


def main(size, filename):
    global height, width
    puzzle = create_initial_puzzle(size)
    # print_puzzle(puzzle)
    if not connected(puzzle):
        puzzle = fix_invalid_islands(puzzle)
    print_puzzle(backtrack(puzzle))


main(sys.argv[1], sys.argv[3])
