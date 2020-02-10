from random import *
import random
import time
import sys


def test_solution(state):
    if -1 in state:
        return False

    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                # print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                # print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                # print(var, "right", compare)
                return False
    return True


def csp(state):

    if test_solution(state):
        return state
    var = get_next_unassigned_var(state)
    for i in get_sorted_values(state, var):
        new_state = state.copy()
        new_state[var] = i
        ret = csp(new_state)
        if ret is not None:
            return ret
    return None


def valid_move(state, val, row):
    for i, num in enumerate(state):
        if i == row or num == -1:
            continue
        if num == val:
            return False
        if (i - num) == (row - val):
            return False
        if i - (len(state) - num) == row - (len(state) - val):
            return False
    return True


def get_next_unassigned_var(state):
    vars = []
    for i in range(0, len(state)):
        if state[i] == -1:
            vars.append(i)
    return vars[random.randint(0, len(vars) - 1)]


def get_sorted_values(state, var):
    moves = []
    for i in range(0, len(state)):
        if valid_move(state, i, var):
            moves.append(i)
    shuffle(moves)
    return moves


def get_min_conflicts(state, threatened_queen_row):
    least_conflict_column = [0 for x in range(len(state))]

    # Column Conflicts
    for column in range(len(state)):
        least_conflict_column[column] += (state.count(column))

    # Diagonal Conflicts
    for column_moving_to in range(len(state)):  # 0, 1, 2, 3
        for queen_compare in range(len(state)):  # 1, 2, 3, 4
            if abs(queen_compare - threatened_queen_row) == abs(state[queen_compare] - column_moving_to):
                least_conflict_column[column_moving_to] += 1

    least_conflict_column[state[threatened_queen_row]] -= 2

    print("Conflicts: " + str(sum(least_conflict_column)))


size = 27
solve_time = 10000
while solve_time > 2:
    start = time.perf_counter()
    state = csp([-1 for i in range(size)])
    end = time.perf_counter()
    solve_time = end - start
    if solve_time < 2:
        print('\n' + str(state))
        print(test_solution(state))
        print(str(solve_time))

    else:
        print('FAIL', end=' ')
