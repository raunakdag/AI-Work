# Raunak Daga
# Othello

import sys
import random

move_numbers = [-11, -10, -9, -1, 1, 9, 10, 11]
board = "??????????" \
        "?........?" \
        "?........?" \
        "?........?" \
        "?...o@...?" \
        "?...@o...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"
black = '@'
white = 'o'


def possible_moves(board, token):
    opposite_token = black if token == white else white

    token_indices = [i for i, ltr in enumerate(board) if ltr == token]
    poss_moves = set()
    for token_index in token_indices:
        for move_number in move_numbers:
            valid_move = False
            current_index_on = token_index + move_number
            while(board[current_index_on] == opposite_token):
                current_index_on += move_number
                valid_move = True
            if board[current_index_on] == '.' and valid_move is True:
                poss_moves.add(current_index_on)
    return sorted(poss_moves)


def move(board, token, move_position):
    opposite_token = black if token == white else white

    token_indices = [i for i, ltr in enumerate(board) if ltr == token]
    flips = set()
    for token_index in token_indices:
        for move_number in move_numbers:
            potential_flips = []
            current_index_on = int(move_position)
            to_continue = True

            if board[current_index_on + move_number] != opposite_token:
                to_continue = False
            else:
                potential_flips.append(current_index_on)
                current_index_on += move_number

            while board[current_index_on] == opposite_token and to_continue:
                potential_flips.append(current_index_on)
                current_index_on += move_number

            if board[current_index_on] == token:
                for flip in potential_flips:
                    flips.add(flip)

    for flip in flips:
        board = board[0: flip] + token + board[flip + 1:]

    return board


def print_board(board):
    print()
    for i in range(0, 100, 10):
        print(board[i: i + 10])
    print()


def current_score(board):
    print('White: ' + str(len([i for i, ltr in enumerate(board) if ltr == white])))
    print('Black: ' + str(len([i for i, ltr in enumerate(board) if ltr == black])))


def percentage(board):
    print('Percent White: ' + str(len([i for i, ltr in enumerate(board) if ltr == white]) / 64))
    print('Percent Black: ' + str(len([i for i, ltr in enumerate(board) if ltr == black]) / 64))


def main(board):
    game_over = False
    turn = black
    all_moves = []
    while game_over is False:
        black_moves = possible_moves(board, black)
        white_moves = possible_moves(board, white)

        # Nobody Can Move
        if len(black_moves) == 0 and len(white_moves) == 0:
            game_over = True

        print(board)
        # current_score(board)
        moves = black_moves if turn == black else white_moves
        if len(moves) != 0:
            # print('Black Possible Moves: ', end='') if turn == black else print(
            #     'White Possible Moves: ', end='')
            # print(moves)

            move_to_make = str(random.choice(moves)) if len(moves) > 0 else 'pass'
            all_moves.append(int(move_to_make))
            # print('I choose ' + str(move_to_make))
            board = move(board, turn, int(move_to_make))
            turn = white if turn == black else black
        elif game_over is True:
            pass
        else:
            # print('Pass')
            all_moves.append(-1)
            turn = white if turn == black else black

    print()
    current_score(board)
    percentage(board)
    print(all_moves)


# main(sys.argv[1])
main(board)
