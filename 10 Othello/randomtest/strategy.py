import time
import random
import math
import sys

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

            if corner_achieved is False:
                if player == white:
                    # max_value_so_far = -math.inf
                    for depth in range(0, 20):
                        max_value_so_far = -math.inf
                        for possibility in possibilities:
                            new_board = move(board, player, possibility)
                            minimized_value = minimize(new_board, depth, -math.inf, math.inf)
                            if minimized_value > max_value_so_far:
                                best_move.value = possibility
                                max_value_so_far = minimized_value

                elif player == black:
                    # min_value_so_far = math.inf
                    for depth in range(0, 20):
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
        if alpha >= beta:  # PRUNING
            return 1000000
        new_board = move(board, white, poss_move)
        alpha = max(alpha, minimize(new_board, depth - 1, alpha, beta))  # PRUNING

    return alpha


def minimize(board, depth, alpha, beta):
    if depth == 0:
        return total_board_heuristic(board)

    poss_moves = possible_moves(board, black)
    for poss_move in poss_moves:
        if alpha >= beta:  # PRUNING
            return -1000000
        new_board = move(board, black, poss_move)
        beta = min(beta, maximize(new_board, depth - 1, alpha, beta))  # PRUNING

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


def board_corners(board):
    heu = 0
    for corner in corners:
        if board[corner] == white:
            heu += 1
        elif board[corner] == black:
            heu -= 1
    return heu


def board_mobility(board):
    moves_white = len(possible_moves(board, white))
    moves_black = len(possible_moves(board, black))

    return moves_white - moves_black


def coin_parity(board):
    heu = 0
    for index in range(len(board)):
        if board[index] == white:
            heu += 1
        elif board[index] == black:
            heu -= 1
    return heu


def total_board_heuristic(board):  # CHANGES
    num = board.count('.')
    # if num >= 32:  # In early game, I'm looking for having as few moves available for my opponent as possible
    if num >= 20:
        return board_mobility(board)
        # print(board_mobility(board))
        # print(board_corners(board))
        # print()
    else:
        # print(board_weight_heuristic(board))
        # print(board_corners(board))
        # print(coin_parity(board))
        # print()
        return board_weight_heuristic(board) * 2 + board_mobility(board)
    # elif num < 32:  # In end game, I'm just looking to win the most amount of pieces
    #     return board_weight_heuristic(board) + board_corners(board) * 30


def main(board, player):
    possibilities = possible_moves(board, player)
    best_move = random.choice(possibilities)
    print(best_move)

    if player == white:
        max_value_so_far = -math.inf
        for depth in range(0, 10):
            for possibility in possibilities:
                new_board = move(board, player, possibility)
                minimized_value = minimize(new_board, depth, -math.inf, math.inf)
                if minimized_value > max_value_so_far:
                    best_move = possibility
                    print(best_move)
                    max_value_so_far = minimized_value

    elif player == black:
        min_value_so_far = math.inf
        for depth in range(0, 10):
            for possibility in possibilities:
                new_board = move(board, player, possibility)
                maximized_value = maximize(new_board, depth, -math.inf, math.inf)
                if maximized_value < min_value_so_far:
                    best_move = possibility
                    print(best_move)
                    min_value_so_far = maximized_value


# main('???????????ooooo...??@ooo@...??o@o@....??..@@@...??..@@@...??.@..@...??........??........???????????', 'o')
main(sys.argv[1], sys.argv[2])
