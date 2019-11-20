import os
import math
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# symbol_set = set()


def get_dimensions(puzzle):
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    size_puzzle = len(puzzle)
    constraint_sets = []
    neighbors = []

    size = int(len(puzzle))  # 81
    N = int(size ** 0.5)  # 9
    factorN = int(N ** 0.5)  # 3

    for factor in range(factorN, 0, -1):
        if N % factor == 0:
            height = factor
            width = N // height
            break

    symbol_set = set()
    for char in "123456789ABCDEFGH"[:N]:
        symbol_set.add(char)


def make_constraints():
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    for width_coord in range(N):
        row_set = set()
        for height_coord in range(N):
            row_set.add(width_coord * N + height_coord)
        constraint_sets.append(row_set)

    for width_coord in range(N):
        column_set = set()
        for height_coord in range(N):
            column_set.add(height_coord * N + width_coord)
        constraint_sets.append(column_set)

    for width_coord in range(width):
        for height_coord in range(height):
            box_set = set()

            for width_coord2 in range(height):
                for height_coord2 in range(width):
                    total = ((width_coord * height) + width_coord2) * \
                        N + (height_coord * width) + height_coord2

                    box_set.add(total)

            constraint_sets.append(box_set)

    for index in range(size_puzzle):
        possible_neighbors = set()
        for constraint_set in constraint_sets:
            if index in constraint_set:
                for constraint in constraint_set:
                    if index != constraint:
                        possible_neighbors.add(constraint)
        # print(index)
        neighbors.append(possible_neighbors)

    # print(constraint_sets)
    # print(neighbors)


def print_puzzle(puzzle):
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    # print()
    for row in range(N):
        row_print = ""

        for column in range(N):
            temp = puzzle[row * N + column]
            row_print = row_print + " " + temp + " "
            if (column + 1) % width == 0:
                row_print = row_print + "|"

        row_print = row_print[:-2].strip()
        print(row_print)

        if (row + 1) % height == 0:
            print(("-") * (len(row_print)))


def get_sorted_values(puzzle, new_spot):
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    possible_symbols = []

    for symbol in symbol_set:
        can_append = True
        for neighbor in neighbors[new_spot]:
            if symbol == puzzle[neighbor]:
                can_append = False
                break
        if can_append:
            possible_symbols.append(symbol)

    return possible_symbols


def get_most_constrained_var(puzzle):
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    most_constrained = []
    index = 0
    for possibility in possibilities:
        if len(possibility) > 1:
            most_constrained.append(index)
        index += 1

    sorted_constrained = sorted(most_constrained)


def csp_backtracking_with_forward_looking(puzzle):
    global size_puzzle
    global N
    global height
    global width
    global symbol_set
    global constraint_sets
    global neighbors
    global possibilities

    if '.' not in puzzle:
        return puzzle

    new_spot = get_most_constrained_var(puzzle)
    for val in get_sorted_values(puzzle, new_spot):
        new_puzzle = assign(puzzle, new_spot, val)
        checked_puzzle = forward_looking(new_puzzle)
        if checked_puzzle is not None:
            result = csp_backtracking_with_forward_looking(checked_puzzle)
            if result is not None:
                return result
    return None


def main(filename):
    if filename is None:
        filename = sys.argv[1]
    puzzle_count = 0
    with open(filename) as file:
        for puzzle in file:
            puzzle = puzzle.replace('\n', '')
            get_dimensions(puzzle)
            # print("Puzzle: ")
            # print_puzzle(puzzle)
            make_constraints()
            # print()
            # print("Solution: ")
            print(csp_backtracking_with_forward_looking(puzzle))
            # print()
            puzzle_count += 1
            # print_puzzle(puzzle)
    # print(puzzle_count)


main('sudoku_puzzles_2_hard.txt')
