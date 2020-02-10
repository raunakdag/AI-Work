import time
import random
import math
black = '@'
white = 'o'
move_numbers = [-11, -10, -9, -1, 1, 9, 10, 11]
board_weight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 8, -3, 4, 2, 2, 4, -3, 8, 0,
                0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
                0, 4, -1, 5, 0, 0, 5, -1, 4, 0,
                0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
                0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
                0, 4, -1, 5, 0, 0, 5, -1, 4, 0,
                0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
                0, 8, -3, 4, 2, 2, 4, -3, 8, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
corners = [11, 18, 81, 88]

# White wants the HIGHEST heuristic
# Black wants the LOWEST heuristic


class Strategy():
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            possibilities = possible_moves(board, player)
            corner_achieved = False
            best_move.value = random.choice(possibilities)
            for possibility in possibilities:
                if possibility in corners:
                    best_move.value = possibility
                    corner_achieved = True

            if not corner_achieved:
                if player == white:
                    for depth in range(0, 10):
                        max_value_so_far = -math.inf
                        for possibility in possibilities:
                            new_board = move(board, player, possibility)
                            minimized_value = minimize(new_board, depth, -math.inf, math.inf)
                            if minimized_value > max_value_so_far:
                                best_move.value = possibility
                                max_value_so_far = minimized_value

                elif player == black:
                    for depth in range(0, 10):
                        min_value_so_far = math.inf
                        for possibility in possibilities:
                            new_board = move(board, player, possibility)
                            maximized_value = maximize(new_board, depth, -math.inf, math.inf)
                            if maximized_value < min_value_so_far:
                                best_move.value = possibility
                                min_value_so_far = maximized_value


def maximize(board, depth, alpha, beta):
    if depth == 0:
        return total_board_heuristic(board)

    poss_moves = possible_moves(board, white)
    for poss_move in poss_moves:
        if alpha >= beta:
            return 1000000
        new_board = move(board, white, poss_move)
        alpha = max(alpha, minimize(new_board, depth - 1, alpha, beta))

    return alpha


def minimize(board, depth, alpha, beta):
    if depth == 0:
        return total_board_heuristic(board)

    poss_moves = possible_moves(board, black)
    for poss_move in poss_moves:
        if alpha >= beta:
            return -1000000
        new_board = move(board, black, poss_move)
        beta = min(beta, maximize(new_board, depth - 1, alpha, beta))

    return beta


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

    return list(poss_moves)


def move(board_given, token, move_position):
    opposite_token = black if token == white else white
    board = str(board_given)
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


def board_weight_heuristic(board):
    weight = 0
    for index in range(len(board)):
        if board[index] == white:
            weight += board_weight[index]
        elif board[index] == black:
            weight -= board_weight[index]
    return weight


def board_mobility(board):
    moves_white = len(possible_moves(board, white))
    moves_black = len(possible_moves(board, black))

    return (moves_white - moves_black)


def coin_parity(board):
    heu = 0
    for index in range(len(board)):
        if board[index] == white:
            heu += 1
        elif board[index] == black:
            heu -= 1
    return heu


def board_corners(board):
    heu = 0
    for corner in corners:
        if board[corner] == white:
            heu += 1
        elif board[corner] == black:
            heu -= 1
    return heu


def total_board_heuristic(board):
    num = board.count('.')
    return board_mobility(board) + board_corners(board) * 20


def test(board, player):
    possibilities = possible_moves(board, player)
    corner_achieved = False
    best_move = random.choice(possibilities)
    for possibility in possibilities:
        if possibility in corners:
            best_move = possibility
            corner_achieved = True

    if not corner_achieved:
        if player == white:
            for depth in range(0, 10):
                max_value_so_far = -math.inf
                for possibility in possibilities:
                    new_board = move(board, player, possibility)
                    minimized_value = minimize(new_board, depth, -math.inf, math.inf)
                    if minimized_value > max_value_so_far:
                        best_move = possibility
                        max_value_so_far = minimized_value

        elif player == black:
            for depth in range(5, 10):
                min_value_so_far = math.inf
                for possibility in possibilities:
                    new_board = move(board, player, possibility)
                    maximized_value = maximize(new_board, depth, -math.inf, math.inf)
                    if maximized_value < min_value_so_far:
                        best_move = possibility
                        min_value_so_far = maximized_value


# test('???????????..o.....??..oo@@..??ooo@@@oo??.oooooo.??..oo@oo.??...oo@oo??...oo@..??....o.@.???????????', '@')
