import time
import random
import math

import os
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))
black = '@'
white = 'o'
move_numbers = [-11, -10, -9, -1, 1, 9, 10, 11]
board_weight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 100, -10, 10, 5, 5, 10, -10, 100, 0,
                0, -10, -50, 3, 3, 3, 3, -50, -10, 0,
                0, 10, 3, 1, 1, 1, 1, 3, 10, 0,
                0, 5, 3, 1, 1, 1, 1, 3, 5, 0,
                0, 5, 3, 1, 1, 1, 1, 3, 5, 0,
                0, 10, 3, 1, 1, 1, 1, 3, 10, 0,
                0, -10, -50, 3, 3, 3, 3, -50, -10, 0,
                0, 100, -10, 10, 5, 5, 10, -10, 100, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]


# White wants the HIGHEST heuristic
# Black wants the LOWEST heuristic
class Strategy():
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            possibilities = possible_moves(board, player)
            best_move.value = random.choice(possibilities)

            if player == white:
                max_value_so_far = -math.inf
                for depth in range(0, 10):
                    for possibility in possibilities:
                        new_board = move(board, player, possibility)
                        if minimize(new_board, depth) > max_value_so_far:
                            best_move.value = possibility
            elif player == black:
                min_value_so_far = math.inf
                for depth in range(0, 10):
                    for possibility in possibilities:
                        new_board = move(board, player, possibility)
                        if maximize(new_board, depth) < min_value_so_far:
                            best_move.value = possibility


def maximize(board, depth):
    if depth == 0:
        return total_board_heuristic(board)

    poss_moves = possible_moves(board, white)
    max_value = -math.inf
    for poss_move in poss_moves:
        new_board = move(board, white, poss_move)
        value = max(max_value, minimize(new_board, depth - 1))

    return max_value


def minimize(board, depth):
    if depth == 0:
        return total_board_heuristic(board)

    poss_moves = possible_moves(board, black)
    min_value = math.inf
    for poss_move in poss_moves:
        new_board = move(board, black, poss_move)
        value = min(min_value, maximize(new_board, depth - 1))

    return min_value


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

    return moves_white - moves_black


def total_board_heuristic(board, token):
    # if board.count('.') > 30:
    #     return board_mobility(board, token)
    # else:
    return board_weight_heuristic(board, token)


total_white_moves = 0
total_black_moves = 0
total_heuristic = 0

with open('test.txt') as file:
    for line in file.readlines():
        line = line.replace('\n', '')
        print(board_weight_heuristic(line))
        print(len(possible_moves(line, white)))
        print(len(possible_moves(line, black)))
        print()
        total_heuristic += board_weight_heuristic(line)
        total_white_moves += len(possible_moves(line, white))
        total_black_moves += len(possible_moves(line, black))

print()
print()
print(total_white_moves)
print(total_black_moves)
print(total_heuristic)
