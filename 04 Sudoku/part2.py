import os
import sys
import copy

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
            for width_2 in range(width, width + subblock_width):
                for height_2 in range(height, height + subblock_height):
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


def fwd_looking(new_possibilities, indices_one_possible_solution):
    global N, sqrtN, symbol_set, constraints, neighbors

    while indices_one_possible_solution:
        index = indices_one_possible_solution.pop()
        for neighbor in neighbors[index]:
            initial_length = len(new_possibilities[neighbor])
            new_possibilities[neighbor] = new_possibilities[neighbor].replace(
                new_possibilities[index], '')
            if initial_length != 1 and len(new_possibilities[neighbor]) == 1:
                indices_one_possible_solution.append(neighbor)
            elif len(new_possibilities[neighbor]) == 0:
                return None

    return new_possibilities


def constraint(new_possibilities):
    global constraints, symbol_set
    if new_possibilities is None:
        return None
    indices_one_possible_solution = []
    for constraint_set in constraints:
        for symbol in symbol_set:
            amt_changes = 0
            change_index = 0
            for value in constraint_set:
                if symbol in new_possibilities[value]:
                    change_index = value
                    amt_changes += 1
            if amt_changes == 0:
                # print('returning none')
                return None
            elif amt_changes == 1:
                new_possibilities[change_index] = symbol
                indices_one_possible_solution.append(change_index)

    return fwd_looking(new_possibilities, indices_one_possible_solution)


def backtrack(possibilities):
    if goal_test(possibilities):
        return possibilities

    next_var = get_most_constrained_var(possibilities)

    for possible_symbol in possibilities[next_var]:
        new_possibilities = possibilities.copy()
        new_possibilities[next_var] = possible_symbol

        checked_board = fwd_looking(new_possibilities, [next_var])
        checked_board = constraint(checked_board)

        if checked_board is not None:
            backtracked_puzzle = backtrack(checked_board)
            if backtracked_puzzle is not None:
                return backtracked_puzzle

    return None


def get_possibilities(puzzle):
    global symbol_set
    possibilities = {}

    for i in range(len(puzzle)):
        if puzzle[i] == '.':
            possibilities[i] = ''.join(symbol_set)
        else:
            possibilities[i] = puzzle[i]

    return possibilities


def get_most_constrained_var(possibilities):
    min_val = 100
    min_index = 0

    for i in range(len(possibilities)):
        if len(possibilities[i]) < min_val and len(possibilities[i]) != 1:
            min_index = i
            min_val = len(possibilities[i])

    return min_index


def goal_test(possibilities):
    for possibility in possibilities:
        if len(possibilities[possibility]) > 1:
            return False
    return True


def compile(final_result):
    str = ''
    for i in final_result:
        str += final_result[i]
    return str


def get_solved(possibilities):
    solved = []
    for i in range(len(possibilities)):
        if len(possibilities[i]) == 1:
            solved.append(i)
    return solved


def main(filename):
    with open(filename) as file:
        for puzzle in file:
            puzzle = puzzle.replace('\n', '')
            set_globals(puzzle)
            make_constraints(puzzle)
            possibilities = get_possibilities(puzzle)
            solved = get_solved(possibilities)
            forwarded = fwd_looking(possibilities, solved)
            constrainted = constraint(forwarded)
            backtracked = backtrack(constrainted)
            compiled = compile(backtracked)
            # print_puzzle(compiled)
            print(compiled)
            # break


# main(sys.argv[1])
main("sudoku_5.txt")
