# Rush Hour
# 9/29/19
import collections

size = 6
space = '0'


def print_puzzle(state):
    for i in range(0, len(state), int(size)):
        print(" ".join(state[i: i + int(size)]))


def swap_characters(s, i1, i2):
    string_list = list(s)
    string_list[i1], string_list[i2] = string_list[i2], string_list[i1]
    return "".join(string_list)


def is_victory(board_state):
    num_zeros = 17 - board_state.rfind('R')
    zero = ''
    for i in range(num_zeros):
        zero.append('0')
    if board_state[board_state.rfind('R')+1:18] == zero:
        return True
    return False


def get_car_moves(board_state, car, direction):
    first_occurence = board_state.find(car)
    last_occurence = board_state.rfind(car)

    car_length = (last_occurence - first_occurence) + 1
    new_board_states = []

    if direction == 'L':
        amount_to_go_left = 1
        while((first_occurence - amount_to_go_left) % 6 != 5):
            append_this = True
            temp_board_state = board_state
            for i in range(car_length):
                if board_state[(first_occurence + i) - amount_to_go_left] != '0':
                    append_this = False
                temp_board_state = swap_characters(
                    temp_board_state, first_occurence + i, (first_occurence + i) - amount_to_go_left)
            new_board_states.append(temp_board_state)
            amount_to_go_left += 1
    if direction == 'R':
        amount_to_go_right = 1
        while((last_occurence + amount_to_go_right) % 6 != 0):
            append_this = True
            temp_board_state = board_state
            for i in range(car_length):
                if board_state[((last_occurence - i) + amount_to_go_right)] != '0':
                    append_this = False
                temp_board_state = swap_characters(
                    temp_board_state, last_occurence - i, (last_occurence - i) + amount_to_go_right)
            new_board_states.append(temp_board_state)
            amount_to_go_right += 1
    if direction == 'U':
        pass
    if direction == 'D':
        pass

    return new_board_states


def get_children(board_state):
    children = []

    cars = list(set(board_state))
    cars.remove('0')

    for car in cars:
        # First check for horizontal or vertical movement
        # Then, within those two, check for moving left/right, and up/down

        first_occurence = board_state.find(car)
        last_occurence = board_state.rfind(car)

        if last_occurence - first_occurence < 5:  # Horizontal
            # Move Left
            if first_occurence % 6 != 0 and board_state[first_occurence - 1] == '0':
                moves = get_car_moves(board_state, car, 'L')
                for move in moves:
                    children.append(move)

            # Move Right
            if last_occurence % 6 != 5 and board_state[last_occurence + 1] == '0':
                moves = get_car_moves(board_state, car, 'R')
                for move in moves:
                    children.append(move)

        else:  # Vertical
            # print(car + " Verical")
            if (first_occurence - 6) >= 0 and board_state[first_occurence - 6] == '0':
                children.append(swap_characters(board_state, last_occurence, first_occurence-6))
            if (last_occurence + 6) <= 35 and board_state[last_occurence + 6] == '0':
                children.append(swap_characters(board_state, first_occurence, last_occurence+6))

    return children


def bfs_shortest_path(board_state):
    fringe = collections.deque()
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    while(fringe):
        current = fringe.pop()
        if(is_victory(current)):
            steps = path(current, parents, size)
            steps.insert(0, board_state.replace('\n', ''))
            return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return None


def path(board_state, parents):
    listmoves = []
    while parents[board_state] != "start":
        listmoves.append(board_state)
        board_state = parents[board_state]
    listmoves = listmoves[::-1]
    for move in listmoves:
        print_puzzle(move, size)
        print()
    return listmoves


# children = get_children('ABBC00ADDC00RREC0F00EGGF00H00F00HIII')
# print_puzzle('ABBC00ADDC00RREC0F00EGGF00H00F00HIII')
# print()
# print_puzzle(children[0])

children = get_children('ABBC00ADDC00RR0C0F000GGF00H00F00HIII')
print("Initial: ")
print_puzzle('ABBC00ADDC00RR0C0F000GGF00H00F00HIII')
print()
for puzzle in children:
    print_puzzle(puzzle)
    print()
