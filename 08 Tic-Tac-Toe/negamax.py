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
    possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']

    move_values = [-10, -10, -10, -10, -10, -10, -10, -10, -10]
    for index in possible_moves:
        new_puzzle = puzzle[0: index] + comp_symbol + puzzle[index + 1:]
        new_comp_symbol = 'O' if comp_symbol == 'X' else 'X'
        # Multiplies initial negamax by -1 because the symbol is changed (above)

        win_or_loss_or_draw = -1 * negamax(new_puzzle, new_comp_symbol)
        if win_or_loss_or_draw == 1:
            move_values[index] = 1
            print('Moving at ' + str(index) + ' results in a ' + 'win!')
        elif win_or_loss_or_draw == 0:
            move_values[index] = 0
            print('Moving at ' + str(index) + ' results in a ' + 'tie!')
        elif win_or_loss_or_draw == -1:
            move_values[index] = -1
            print('Moving at ' + str(index) + ' results in a ' + 'loss!')

    final_index = -1

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


# The negamax function
# Runs from computer_move
def negamax(puzzle, comp_symbol):
    # This checks if somebody has won (returns symbol), tied (returns 'tie')
    # The ifs check to see if anybody has won; if the won and current symbol
    # are the same, then return 1 and vice versa. Return 0 for tie.
    over = check_terminal_state(puzzle)
    if over == 'X' and comp_symbol == 'X':
        return 1
    elif over == 'X' and comp_symbol == 'O':
        return -1
    elif over == 'O' and comp_symbol == 'X':
        return -1
    elif over == 'O' and comp_symbol == 'O':
        return 1
    elif over == 'tie':
        return 0

    # Get every possible move by iterating over .'s
    possible_moves = [i for i, ltr in enumerate(puzzle) if ltr == '.']
    max_value = -1000  # Arbitrary max value
    for move in possible_moves:
        new_puzzle = puzzle[0: move] + comp_symbol + puzzle[move + 1:]  # Creating new puzzle
        # If the value returned by negamax is greater than current max, replace current max with said value.
        # Negamax multiplies the returned value by -1 to ensure that if a win occurs for the next symbol,
        # it shows up as a loss for the current symbol. Additionally, the ternary operator changes
        # the symbol to be the opposite symbol.
        max_value = max(max_value, -1 * negamax(new_puzzle, 'X' if comp_symbol == 'O' else 'O'))

    return max_value


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
        return 'tie'
    return None


def current_board(puzzle):
    print('Current board: ')
    print(puzzle[0: 3] + '    ' + '012')
    print(puzzle[3: 6] + '    ' + '345')
    print(puzzle[6: 9] + '    ' + '678')
    print()


def main():
    next_player, comp_symbol, user_symbol, puzzle = 'c', 'X', 'O', sys.argv[1]
    if 'X' in puzzle or 'O' in puzzle:
        amt_x, amt_o = puzzle.count('X'), puzzle.count('O')
        comp_symbol = 'O' if amt_x > amt_o else 'X'
        user_symbol = 'X' if amt_x > amt_o else 'O'
        next_player = 'c'
    else:
        first = input("Should I be X or O? ")
        next_player = 'c' if first == 'X' else 'u'
        comp_symbol = 'X' if first == 'X' else 'O'
        user_symbol = 'O' if first == 'X' else 'X'

    while '.' in puzzle:
        current_board(puzzle)

        if next_player == 'c':
            puzzle = computer_move(puzzle, comp_symbol)
            next_player = 'u'
        elif next_player == 'u':
            puzzle = user_move(puzzle, user_symbol)
            next_player = 'c'

        winner = check_terminal_state(puzzle)
        if winner != '.' and winner is not None:
            if winner == comp_symbol:
                current_board(puzzle)
                print('I win!')
                exit()
            elif winner == user_symbol:
                current_board(puzzle)
                print('You win!')
                exit()

    current_board(puzzle)
    print('We tied!')


main()
