import sys


def user_move(puzzle, user_symbol):

    possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']

    final_str = ''
    for move in possible_moves:
        final_str += str(move) + ', '

    print('You can move to any of these possible spaces: ' + final_str[:-2] + '.')
    choice = int(input('Your choice? '))
    print()
    puzzle = puzzle[0: choice] + user_symbol + puzzle[choice + 1:]

    return puzzle


def computer_move(puzzle, comp_symbol):
    # Analyze Possible Computer Moves
    possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']

    move_values = [-10, -10, -10, -10, -10, -10, -10, -10, -10]
    for index in possible_moves:
        new_puzzle = puzzle[0: index] + comp_symbol + puzzle[index + 1:]
        win_or_loss_or_draw = minimax(new_puzzle, comp_symbol)
        what_to_print = ''
        if win_or_loss_or_draw == 0:
            move_values[index] = 0
            what_to_print = 'tie!'
            # print(new_puzzle + " " + str(comp_symbol))
        elif win_or_loss_or_draw == 1 and comp_symbol == 'X':
            move_values[index] = 1
            what_to_print = 'win!'
        elif win_or_loss_or_draw == -1 and comp_symbol == 'O':
            move_values[index] = 1
            what_to_print = 'win!'
        elif win_or_loss_or_draw == -1 and comp_symbol == 'X':
            move_values[index] = -1
            what_to_print = 'loss!'
        elif win_or_loss_or_draw == 1 and comp_symbol == 'O':
            move_values[index] = -1
            what_to_print = 'loss!'
        else:
            move_values[index] = -1
            what_to_print = 'loss!'

        print('Moving at ' + str(index) + ' results in a ' + what_to_print)

    final_index = -1

    # print('Move Values:', end='')
    # print(move_values)
    # print()

    if 1 in move_values:
        final_index = move_values.index(1)
    elif 0 in move_values:
        final_index = move_values.index(0)
    else:
        final_index = move_values.index(-1)

    print('I choose space ' + str(final_index) + '.')
    print()

    puzzle = puzzle[0: final_index] + comp_symbol + puzzle[final_index + 1:]

    return puzzle


def minimax(new_puzzle, comp_symbol):
    value = 5
    if comp_symbol == 'O':
        value = maximize(new_puzzle)
    else:
        value = minimize(new_puzzle)
    return value


def maximize(puzzle):
    over = check_terminal_state(puzzle)
    if over == 'X':
        return 1
    elif over == 'O':
        return -1
    elif over == -1:
        return 0
    else:
        possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']
        possible_board_states = []
        for move in possible_moves:
            new_puzzle = puzzle[0: move] + 'X' + puzzle[move + 1:]
            possible_board_states.append(new_puzzle)

        max_value = -1000
        for board_state in possible_board_states:
            value = minimize(board_state)
            # if board_state == 'OXXOOXXOX':
            #     print("Value: " + str(value))
            if value > max_value:
                max_value = value

        # print("Board States")
        # for board in possible_board_states:
        #     current_board(board)
        # print("Max Value" + str(max_value))
        return max_value


def minimize(puzzle):
    over = check_terminal_state(puzzle)
    if over == 'X':
        return 1
    elif over == 'O':
        return -1
    elif over == -1:
        return 0
    else:
        possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']
        possible_board_states = []
        for move in possible_moves:
            new_puzzle = puzzle[0: move] + 'O' + puzzle[move + 1:]
            possible_board_states.append(new_puzzle)

        min_value = 1000
        for board_state in possible_board_states:
            value = maximize(board_state)
            if value < min_value:
                min_value = value

        # print("Board States")
        # for board in possible_board_states:
        #     current_board(board)
        # print("Min Value" + str(min_value))
        return min_value


def check_terminal_state(puzzle):
    if puzzle[0] == puzzle[1] == puzzle[2]:
        return puzzle[0]
    if puzzle[3] == puzzle[4] == puzzle[5]:
        return puzzle[3]
    if puzzle[6] == puzzle[7] == puzzle[8]:
        return puzzle[6]
    if puzzle[0] == puzzle[3] == puzzle[6]:
        return puzzle[0]
    if puzzle[1] == puzzle[4] == puzzle[7]:
        return puzzle[1]
    if puzzle[2] == puzzle[5] == puzzle[8]:
        return puzzle[2]
    if puzzle[0] == puzzle[4] == puzzle[8]:
        return puzzle[0]
    if puzzle[2] == puzzle[4] == puzzle[6]:
        return puzzle[2]
    if '.' not in puzzle:
        return -1
    return None


def current_board(puzzle):
    print('Current board: ')
    print(puzzle[0: 3] + '    ' + '012')
    print(puzzle[3: 6] + '    ' + '345')
    print(puzzle[6: 9] + '    ' + '678')
    print()


def main():
    # puzzle, user = sys.argv[1], ''
    next_player, comp_symbol, user_symbol, puzzle = 'c', 'X', 'O', sys.argv[1]
    if 'X' in puzzle or 'O' in puzzle:
        amt_x = puzzle.count('X')
        amt_o = puzzle.count('O')
        if amt_x > amt_o:
            comp_symbol = 'O'
            user_symbol = 'X'
        else:
            comp_symbol = 'X'
        next_player = 'c'
    else:
        first = input("Should I be X or O? ")
        if first == 'X':
            next_player = 'c'
            comp_symbol = 'X'
            user_symbol = 'O'
        else:
            next_player = 'u'  # User
            comp_symbol = 'O'
            user_symbol = 'X'

    while '.' in puzzle:
        current_board(puzzle)

        if next_player == 'c':
            puzzle = computer_move(puzzle, comp_symbol)
            next_player = 'u'

            winner = check_terminal_state(puzzle)
            if winner != '.' and winner is not None:
                if winner == comp_symbol:
                    current_board(puzzle)
                    print('I win!')
                elif winner == user_symbol:
                    current_board(puzzle)
                    print('You win!')
                exit()

        elif next_player == 'u':
            puzzle = user_move(puzzle, user_symbol)
            next_player = 'c'

            winner = check_terminal_state(puzzle)
            if winner != '.' and winner is not None:
                if winner == comp_symbol:
                    current_board(puzzle)
                    print('I win!')
                elif winner == user_symbol:
                    current_board(puzzle)
                    print('You win!')
                exit()

    print('We tied!')


#
main()

# current_board('OXX.X.OO.')
# minimax('OXX.X.OO.', 'O')
# print(minimax('OXX.O.XOX', 'O'))
