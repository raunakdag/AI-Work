import time
import random
import math
black = '@'
white = 'o'
move_numbers = [-11, -10, -9, -1, 1, 9, 10, 11]
board_weight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 4, -3, 2, 2, 2, 2, -3, 4, 0,
                0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
                0, 2, -1, 1, 0, 0, 1, -1, 2, 0,
                0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
                0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
                0, 2, -1, 1, 0, 0, 1, -1, 2, 0,
                0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
                0, 4, -3, 2, 2, 2, 2, -3, 4, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
corners = [11, 18, 81, 88]

# White wants the HIGHEST heuristic
# Black wants the LOWEST heuristic


class Strategy():
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            possibilities = possible_moves(board, player)
            best_move.value = random.choice(possibilities)

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
    return weight/10


def actual_board_mobility(board):
    heu = 0
    moves_white = len(possible_moves(board, white))
    moves_black = len(possible_moves(board, black))

    if moves_white + moves_black != 0:
        heu = 100 * ((moves_white - moves_black) / (moves_white + moves_black))

    return heu


def potential_board_mobility(board):
    white_token_indices = [i for i, ltr in enumerate(board) if ltr == white]
    black_token_indices = [i for i, ltr in enumerate(board) if ltr == black]

    white_potential = 0
    for token_index in white_token_indices:
        for direction in move_numbers:
            if board[token_index + direction] == '.':
                white_potential += 1

    black_potential = 0
    for token_index in black_token_indices:
        for direction in move_numbers:
            if board[token_index + direction] == '.':
                black_potential += 1

    heu = 0
    if white_potential + black_potential != 0:
        heu = 100 * ((white_potential - black_potential) / (white_potential + black_potential))

    return heu


def coin_parity(board):
    max_player_coins, min_player_coins = 0, 0
    for index in range(len(board)):
        if board[index] == white:
            max_player_coins += 1
        elif board[index] == black:
            min_player_coins += 1
    return 100 * ((max_player_coins - min_player_coins) / (max_player_coins + min_player_coins))


def board_corners(board):
    white_corners = 0
    black_corners = 0
    for corner in corners:
        if board[corner] == white:
            white_corners += 1
        elif board[corner] == black:
            black_corners += 1

    heu = 0
    if white_corners + black_corners != 0:
        heu = 100 * ((white_corners - black_corners) / (white_corners + black_corners))

    return heu


def corner_closeness(board):
    next_to_corners = [12, 21, 22, 17, 27, 28, 71, 72, 82, 77, 78, 87]


def stability(board):
    pass


def total_board_heuristic(board):
    if board.count('.') > 32:
        # + potential_board_mobility(board) * 25
        return board_corners(board) * 10 + actual_board_mobility(board) * 25
    elif board.count('.') <= 32:
        return board_corners(board) * 30 + coin_parity(board) * 10
