def get_shortest_word(puzzle, index):
    i = 3
    while True:
        string_horizontal = r'-' * i
        regex_match = re.search(string_horizontal, puzzle)
        if regex_match:
            return regex_match.span()

        string_vertical = r'-' + (r'{-#\w}' * width)
        regex_match = re.search(string_vertical, puzzle)
        if regex_match:
            return regex_match.span()

        i += 1
def get_all_indexes_old(puzzle):
    global width, height, len_p, num_blocked
    indexes = []
    for i in range(len(puzzle)):
        if puzzle[i] == '-' and puzzle[opposite(i)] == '-':
            if num_blocked % 2 == 0 and len_p // 2 == i:
                pass
            else:
                indexes.append(i)

    final_indexes = []
    for index in indexes:
        horizontal = True
        vertical = True

        block_row = index // width
        block_col = index % width

        # Left. Checks if in leftmost column and square on direct left is not blocking square.
        if index % width != 0 and puzzle[index - 1] != '#':
            for i in range(index - 1, index - 4, -1):
                if i < 0 or puzzle[i] == '#' or (i // width) != block_row:
                    horizontal = False

        # Right
        if index % width != (width - 1) and puzzle[index + 1] != '#':
            for i in range(index + 1, index + 4, 1):
                # print(i)
                if i >= height * width or puzzle[i] == '#' or (i // width) != block_row:
                    horizontal = False

        # Up/North
        if index // width != 0 and puzzle[index - width] != '#':
            for i in range(index - width, index - 4 * width, -width):
                if i < 0 or puzzle[i] == '#':
                    vertical = False

        # Down/South
        if index // width != (height - 1) and puzzle[index + width] != '#':
            for i in range(index + width, index + 4 * width, width):
                if i >= height * width or puzzle[i] == '#':
                    vertical = False

        if horizontal and vertical:
            final_indexes.append(index)

    return final_indexes


def character_limit(puzzle):
    global width, height
    indexes_non_blocking = []
    for i in range(len(puzzle)):
        if puzzle[i] != '#':
            indexes_non_blocking.append(i)

    for index in indexes_non_blocking:
        horizontal = False
        vertical = False

        block_row = index // width
        block_col = index % width

        # Left. Checks if in the third column or more, if goes two characters
        # succesfully, then set horizontal to true.
        if index % width >= 2:
            temp_bool = True
            for i in range(index - 1, index - 3, -1):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                horizontal = True

        # Middle Horizontal
        if index % width >= 1 and index % width <= (width - 2):
            temp_bool = True
            for i in range(index - 1, index + 2, 1):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                horizontal = True

        # Right
        if index % width <= (width - 3):
            temp_bool = True
            for i in range(index + 1, index + 3, 1):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                horizontal = True

        # Up/North 2
        if index // width >= 2:
            temp_bool = True
            for i in range(index - width, index - 3 * width, -width):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                vertical = True

        # Middle Vertical
        if index // width >= 1 and index // width <= (height - 2):
            temp_bool = True
            for i in range(index - width, index + 2 * width, width):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                vertical = True

        # Down/South 2
        if index // width <= (height - 3):
            temp_bool = True
            for i in range(index + 1 * width, index + 3 * width, width):
                if puzzle[i] == '#':
                    temp_bool = False
            if temp_bool:
                vertical = True

        if not horizontal or not vertical:
            return False

    return True

def old_implied_closeby():
    # Checking if a blocking character is close by horizontally
    print('Index im checking' + str(index))
    for direction in directions_horizontal:
        amt_gone = 2
        index_to_change_till = 0
        while amt_gone < 4:
            new_index = index + amt_gone * direction
            index_to_change_till = new_index
            if new_index > 0 and new_index < len_p and puzzle[new_index] == '#':
                if (new_index) // width == block_row:
                    for index_add in range(index + direction, index_to_change_till, direction):
                        print(puzzle[index_add])
                        if puzzle[index_add] == '-':
                            to_be_implied.add(index_add)
                        else:
                            return None
                    break
            amt_gone += 1

    # Checking if a blocking character is close by vertically
    for direction in directions_vertical:
        amt_gone = 2
        index_to_change_till = 0
        while amt_gone < 4:
            new_index = index + amt_gone * direction
            index_to_change_till = new_index
            if new_index > 0 and new_index < len_p:
                if puzzle[new_index] == '#':
                    for index_add in range(index + direction, index_to_change_till, direction):
                        if puzzle[index_add] == '-':
                            to_be_implied.add(index_add)
                        else:
                            return None
                    break
            amt_gone += 1

def new_implied_closeby():
    if puzzle[index - 2] == '#' or puzzle[index - 3] == '#':
        if puzzle[index - 2] == '#':
            if puzzle[index - 1] == '-' and ((index - 1) // width) == block_row:
                to_be_implied.add(index - 1)
        if puzzle[index - 3] == '#':
            if puzzle[index - 1] == '-' and puzzle[index - 2] == '-' and ((index - 1) // width) == block_row and ((index - 2) // width) == block_row:
                to_be_implied.add(index - 1)
                to_be_implied.add(index - 2)

    if puzzle[index + 2] == '#' or puzzle[index + 3] == '#':
        if puzzle[index + 2] == '#':
            pass
        if puzzle[index + 3] == '#':
            pass


# Checks to see if the entire board is 180 degrees rotationally symmetric. Palindromic.
def symmetric(puzzle):
    for i in range(len(puzzle)):
        if puzzle[i] != '#':
            puzzle = puzzle[0: i] + '!' + puzzle[i + 1:]

    return True if puzzle == puzzle[::-1] else False
