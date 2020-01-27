import os
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def set_globals(puzzle):
    global N, sqrtN, subblock_height, subblock_width, symbol_set, constraints, neighbors

    N = len(puzzle)
    sqrtN = int(N ** 0.5)

    start_subblock_height = int((N ** 0.5) ** 0.5)
    for possibility in range(start_subblock_height, 0, -1):
        if sqrtN % possibility == 0:
            subblock_height = possibility
            break

    subblock_width = int(sqrtN / subblock_height)

    symbol_set = set()
    for char in "123456789ABCDEFGH"[:int(N ** 0.5)]:
        symbol_set.add(char)


def make_constraints(puzzle):
    global N, sqrtN, subblock_height, subblock_width, symbol_set, constraints, neighbors

    constraints = []
    neighbors = []

    # Row Constraint Sets
    for width in range(sqrtN):
        constraint = set()
        for height in range(sqrtN):
            constraint.add(width * sqrtN + height)
        constraints.append(constraint)

    # Column Constraint Sets
    for width in range(sqrtN):
        constraint = set()
        for height in range(sqrtN):
            constraint.add(width + sqrtN * height)
        constraints.append(constraint)

    # Block Constraint Sets
    for width in range(0, sqrtN, subblock_width):  # 0, 3, 6
        for height in range(0, sqrtN, subblock_height):  # 0, 3, 6
            neighbor_set = set()
            for width_2 in range(width, width + 3):
                for height_2 in range(height, height + 3):
                    # print("Width 2: " + str(width_2) + " Height 2: " + str(height_2))
                    neighbor_set.add(width_2 + height_2 * sqrtN)

            constraints.append(neighbor_set)

    # FINISH NEIGHBOR SETS
    for index in range(N):
        possible_neighbors = set()
        for constraint_set in constraints:
            if index in constraint_set:
                for constraint in constraint_set:
                    if index != constraint:
                        possible_neighbors.add(constraint)
        neighbors.append(possible_neighbors)


def print_puzzle(puzzle):
    global N, sqrtN, subblock_height, subblock_width, symbol_set

    lines = [puzzle[i: i + sqrtN] for i in range(0, len(puzzle), sqrtN)]

    index = 0
    for line in lines:
        line = '|'.join(line[i:i + subblock_width]
                        for i in range(0, len(line), subblock_width))
        line = ' '.join(line)
        lines[index] = line
        index += 1

    index = 0
    for line in lines:
        index += 1
        print(line)
        if index % subblock_height == 0:
            print('-' * len(line))


def amt_symbols(puzzle):
    global symbol_set
    symbols = {}
    for symbol in symbol_set:
        symbols[symbol] = puzzle.count(symbol)
    print(symbols)


def backtrack(puzzle):
    global N, sqrtN, subblock_height, subblock_width, symbol_set, constraints, neighbors
    if '.' not in puzzle:
        return puzzle

    next_available_var = puzzle.find('.')

    for value in get_sorted_values(puzzle, next_available_var):
        new_puzzle = puzzle[:next_available_var] + str(value) + puzzle[next_available_var + 1:]
        solution = backtrack(new_puzzle)
        if solution is not None:
            return solution
    return None


def get_sorted_values(puzzle, index_of_var):
    global N, sqrtN, subblock_height, subblock_width, symbol_set, constraints, neighbors

    possible_symbols = []

    for symbol in symbol_set:
        can_append = True
        for neighbor in neighbors[index_of_var]:
            if symbol == puzzle[neighbor]:
                can_append = False
                break
        if can_append:
            possible_symbols.append(symbol)

    return possible_symbols
    # FINISH GETTING THE SORTED VALUES


def main(filename):
    if filename is None:
        filename = sys.argv[1]
    with open(filename) as file:
        # line = 0
        for puzzle in file:
            print(str(line))
            # line += 1
            puzzle = puzzle.replace('\n', '')
            set_globals(puzzle)
            # amt_symbols(puzzle)
            # print("Puzzle: ")
            # print_puzzle(puzzle)
            make_constraints(puzzle)
            # break
            print()
            print("Solution: ", end='')
            print(backtrack(puzzle))
            # print()
            # print_puzzle(puzzle)


main('sudoku_puzzles_1.txt')
