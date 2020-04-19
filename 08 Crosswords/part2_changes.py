import sys
import re
import random
import os

# Change current working directory, only needed for Atom
# os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
        word = seedstring[seedstring.rfind(str(y)) + len(str(y)):].lower()
        start = convert(x, y)

        if direction == 'V':
            for i in range(len(word)):
                if word[i] == '#':
                    puzzle = implied(puzzle, start + width * i)
                puzzle = place_at_index(
                    puzzle, word[i].lower(), start + width * i)
        elif direction == 'H':
            for i in range(len(word)):
                if word[i] == '#':
                    puzzle = implied(puzzle, start + i)
                puzzle = place_at_index(puzzle, word[i].lower(), start + i)

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

def make_dictionary(filename):
    global patterns, letter_count
    patterns, letter_count = {}, {}

    with open(filename) as words_text:
        for word in words_text:
            word = word.replace('\n', '').rstrip().lower()

            len_w = len(word)
            if str.isalpha(word) and len_w >= 3:
                # All Blanks
                if '-' * len_w in patterns:
                    patterns['-' * len_w].add(word)
                else:
                    patterns['-' * len_w] = set([word])

                for index in range(len_w):
                    # One Blank at Each
                    p_match = place_at_index('-' * len_w, word[index], index)
                    if p_match in patterns:
                        patterns[p_match].add(word)
                    else:
                        patterns[p_match] = set([word])

                    # letter Count
                    if word[index] not in letter_count:
                        letter_count[word[index]] = 1
                    else:
                        letter_count[word[index]] += 1


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

    if block_col <= 2:
        if block_col == 1:
            to_be_implied.add(index - 1)
        if block_col == 2:
            to_be_implied.add(index - 2)
            to_be_implied.add(index - 1)

    if block_col >= (width - 3):
        if block_col == (width - 2):
            to_be_implied.add(index + 1)
        if block_col == (width - 3):
            to_be_implied.add(index + 2)
            to_be_implied.add(index + 1)

    if block_row <= 2:
        if block_row == 1:
            to_be_implied.add(index - width)
        if block_row == 2:
            to_be_implied.add(index - width)
            to_be_implied.add(index - 2 * width)

    if block_row >= (height - 3):
        if block_row == (height - 2):
            to_be_implied.add(index + width)
        if block_row == (height - 3):
            to_be_implied.add(index + 2 * width)
            to_be_implied.add(index + width)

    for index_to_do in to_be_implied:
        if num_blocked % 2 == 0 and len_p // 2 == index_to_do and len_p % 2 == 1:
            return None
        if puzzle is not None:
            puzzle = implied(puzzle, index_to_do)

    return puzzle

def backtrack(puzzle):
    # print_puzzle(puzzle)
    global height, width, num_blocked
    if not connected(puzzle) or puzzle.count('#') > num_blocked:
        return None
    if puzzle.count('#') == num_blocked:
        return puzzle

    possible_indexes = get_blanks(puzzle)
    list.sort(possible_indexes, key=lambda index: blocking_square_heuristic(
        puzzle, index), reverse=True)
    for new_index in possible_indexes:
        new_puzzle = implied(puzzle, new_index)
        if new_puzzle is not None:
            backtracked_puzzle = backtrack(new_puzzle)
            if backtracked_puzzle is not None:
                return backtracked_puzzle

    return None


def crossword_backtrack(puzzle, used_words, h_dict, v_dict):
    global letter_count
    print_puzzle(puzzle)
    if '-' not in puzzle:
        return puzzle
    if puzzle is None:
        return None

    mci, direction, poss_words, implied_indices = find_most_constrained(
        puzzle, h_dict, v_dict)
    if mci is None:
        return None

    h_dict_new = h_dict.copy()
    v_dict_new = v_dict.copy()
    if direction == 'H':
        h_dict_new.pop(mci)
    else:
        v_dict_new.pop(mci)

    poss_words = list(poss_words)
    list.sort(poss_words, key=lambda word: sum(
        letter_count[ch] for ch in word), reverse=True)
    for word in poss_words:
        if word not in used_words:
            # print("Word being placed: " + word)
            new_used_words = used_words.copy()
            new_used_words.add(word)

            new_puzzle = place_word(puzzle, mci, direction, word)
            # print_puzzle(new_puzzle)
            illegal = check_illegal(
                new_puzzle, implied_indices, direction, used_words)
            if illegal:
                continue

            new_puzzle = crossword_backtrack(
                new_puzzle, new_used_words, h_dict_new, v_dict_new)
            if new_puzzle is not None:
                return new_puzzle

    return None

def blocking_square_heuristic(puzzle, i):
    global width, len_p
    block_row, block_col = i // width, i % width
    num_up = num_down = num_left = num_right = 1

    if (i - width >= 0):
        while(i - num_up * width >= 0 and puzzle[i - num_up * width] != '#'):
            num_up += 1

    if (i + width < len_p):
        while(i + num_down * width < len_p and puzzle[i + num_down * width] != '#'):
            num_down += 1

    if (i - 1 >= 0):
        while(i - num_left >= 0 and (i - num_left) // width == block_row and puzzle[i - num_left] != '#'):
            num_left += 1

    if (i + 1 < len_p):
        while(i + num_right < len_p and (i + num_right) // width == block_row and puzzle[i + num_right] != '#'):
            num_right += 1

    return num_left * num_right + num_up * num_down


def check_illegal(puzzle, implied_indices, direction, used_words):
    global width, len_p
    implied_words = []
    if direction == 'H':
        for i in implied_indices:
            block_row, block_col = i // width, i % width
            vertical_word = ''

            if (i - width >= 0):
                num_up = 1
                while(i - num_up * width >= 0 and puzzle[i - num_up * width] != '#'):
                    vertical_word = puzzle[i - num_up * width] + vertical_word
                    num_up += 1

            vertical_word = vertical_word + puzzle[i]

            if (i + width < len_p):
                num_down = 1
                while(i + num_down * width < len_p and puzzle[i + num_down * width] != '#'):
                    vertical_word += puzzle[i + num_down * width]
                    num_down += 1

            if vertical_word and '#' not in vertical_word:
                implied_words.append(vertical_word)

    elif direction == 'V':
        for i in implied_indices:
            block_row, block_col = i // width, i % width
            horizontal_word = ''

            if (i - 1 >= 0):
                num_left = 1
                while(i - num_left >= 0 and (i - num_left) // width == block_row and puzzle[i - num_left] != '#'):
                    horizontal_word = puzzle[i - num_left] + horizontal_word
                    num_left += 1

            horizontal_word = horizontal_word + puzzle[i]

            if (i + 1 < len_p):
                num_right = 1
                while(i + num_right < len_p and (i + num_right) // width == block_row and puzzle[i + num_right] != '#'):
                    horizontal_word += puzzle[i + num_right]
                    num_right += 1

            if horizontal_word and '#' not in horizontal_word:
                implied_words.append(horizontal_word)

    for word in implied_words:
        count_pre_letters = 0
        for i in range(len(word)):
            if word[i] != '-':
                count_pre_letters += 1

        pattern_set = []
        if count_pre_letters > 1:
            pattern_set = get_1_char_patterns(word)
        else:
            pattern_set.append(word)

        total_word_count = 0
        if len(pattern_set) == 0:
            continue
        if len(pattern_set) == 1:
            if pattern_set[0] in patterns:
                total_word_count = len(patterns[pattern_set[0]])
            else:
                continue
        else:
            words = set_intersection(pattern_set)
            if words is None:
                return True
            total_word_count = len(words)

        if total_word_count == 0:
            return True

    return False

def find_word_locations_at_beginning(puzzle):
    global width, height, len_p

    h, v = {}, {}
    for i in range(len(puzzle)):
        block_row, block_col = i // width, i % width
        h_v = []

        # Horizontal
        if (block_col == 0 or (i - 1 >= 0 and puzzle[i - 1] == '#')) and (puzzle[i] != '#' and block_col < width - 2):
            num_to_right = 0
            while(i + num_to_right < len_p and puzzle[i + num_to_right] != '#' and (i + num_to_right) // width == block_row):
                num_to_right += 1
            if num_to_right >= 3:
                h_v.append(num_to_right)
        if len(h_v) == 0:
            h_v.append(None)

        # Vertical
        if (block_row == 0 or (i - width >= 0 and puzzle[i - width] == '#')) and (puzzle[i] != '#' and block_row < height - 2):
            num_down = 0
            while(i + num_down * width < len_p and puzzle[i + num_down * width] != '#'):
                num_down += 1
            if num_down >= 3:
                h_v.append(num_down)
        if len(h_v) == 1:
            h_v.append(None)

        if h_v[0] is not None:
            h[i] = (h_v[0])
        if h_v[1] is not None:
            v[i] = (h_v[1])

    return h, v

def find_most_constrained(puzzle, h_dict, v_dict):
    global width, height, len_p, patterns
    cli = [0, 'H', None, None]  # Temp
    min_word_amt = 100000000  # Arbitrary High Amount

    for index in h_dict:
        len_fwd = h_dict[index]
        word = puzzle[index: index + len_fwd]

        implied_indices = []
        for i in range(index, index + len_fwd):
            implied_indices.append(i)

        cli_compare = [index, 'H']
        if '-' not in word:
            continue

        count_pre_letters = 0
        for i in range(len(word)):
            if word[i] != '-':
                count_pre_letters += 1

        pattern_set = []
        if count_pre_letters > 1:
            pattern_set = get_1_char_patterns(word)
        else:
            pattern_set.append(word)

        total_word_count = 0
        if len(pattern_set) == 0:
            continue
        if len(pattern_set) == 1:
            if pattern_set[0] in patterns:
                total_word_count = len(patterns[pattern_set[0]])
                cli_compare.append(patterns[pattern_set[0]])
            else:
                continue
        else:
            words = set_intersection(pattern_set)
            if words is None:
                continue
            cli_compare.append(words)
            total_word_count = len(words)

        cli_compare.append(implied_indices)

        cli = cli_compare if total_word_count < min_word_amt else cli
        min_word_amt = total_word_count if total_word_count < min_word_amt else min_word_amt

    for index in v_dict:
        len_fwd = v_dict[index]
        word = puzzle[index: index + len_fwd * width: width]

        implied_indices = []
        for i in range(index, index + len_fwd * width, width):
            implied_indices.append(i)

        cli_compare = [index, 'V']
        if '-' not in word:
            continue

        count_pre_letters = 0
        for index in range(len(word)):
            if word[index] != '-':
                count_pre_letters += 1

        pattern_set = []
        if count_pre_letters > 1:
            pattern_set = get_1_char_patterns(word)
        else:
            pattern_set.append(word)

        total_word_count = 0
        if len(pattern_set) == 0:
            continue
        if len(pattern_set) == 1:
            if pattern_set[0] in patterns:
                total_word_count = len(patterns[pattern_set[0]])
                cli_compare.append(patterns[pattern_set[0]])
            else:
                continue
        else:
            words = set_intersection(pattern_set)
            if words is None:
                continue
            cli_compare.append(words)
            total_word_count = len(words)

        cli_compare.append(implied_indices)

        cli = cli_compare if total_word_count < min_word_amt else cli
        min_word_amt = total_word_count if total_word_count < min_word_amt else min_word_amt

    if cli == [0, 'H', None, None]:
        return None, None, None, None
    else:
        return cli[0], cli[1], cli[2], cli[3]

def get_1_char_patterns(word):
    # Word must have 2 non blank letters or more
    index_of_letters = []
    for i in range(len(word)):
        if word[i] != '-':
            index_of_letters.append(i)

    pattern_list = []
    for index in index_of_letters:
        base_pattern = '-' * len(word)
        base_pattern = place_at_index(base_pattern, word[index], index)
        pattern_list.append(base_pattern)

    return pattern_list

def get_blanks(puzzle):
    indexes = []
    for i in range(len(puzzle)):
        if puzzle[i] == '-' and puzzle[opposite(i)] == '-':
            if num_blocked % 2 == 0 and len_p // 2 == i:
                pass
            else:
                indexes.append(i)
    return indexes


# ----------------------------- HELPER METHODS --------------------  #

def set_intersection(pattern_set):
    global patterns
    words = None
    if pattern_set[0] in patterns:
        words = patterns[pattern_set[0]]
    else:
        return None
    for i in range(1, len(pattern_set)):
        if pattern_set[i] in patterns:
            words = patterns[pattern_set[i]].intersection(words)
        else:
            return None
    return words

def convert(x, y):
    global width
    return x * width + y

def opposite(index):
    global len_p
    return len_p - index - 1

def place_at_index(string, char, index):
    return string[0: (index)] + char + string[(index) + 1:]

def place_word(puzzle, mci, direction, word):
    global width
    if direction == 'H':
        for i in range(len(word)):
            puzzle = place_at_index(puzzle, word[i], mci + i)
    elif direction == 'V':
        for i in range(len(word)):
            puzzle = place_at_index(puzzle, word[i], mci + width * i)

    return puzzle

def print_puzzle(puzzle):
    global width
    new_puzzle = ''
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
    global height, width, letter_count
    puzzle = create_initial_puzzle(size)
    make_dictionary(filename)
    if not connected(puzzle):
        puzzle = fix_invalid_islands(puzzle)
    puzzle = backtrack(puzzle)
    print_puzzle(puzzle)
    h, v = find_word_locations_at_beginning(puzzle)
    crossword_backtrack(puzzle, set(), h, v)


main(sys.argv[1], sys.argv[3])
