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


size = 35
start = time.perf_counter()
solution = (csp([-1 for i in range(size)]))
end = time.perf_counter()
solve_time = end - start
print(solution)
print(test_solution(solution))
print(str(solve_time))


# while solve_time < 4:
#     start = time.perf_counter()
#     state = csp([-1 for i in range(size)])
#     end = time.perf_counter()
#     solve_time = end - start
#     print('FAIL', end=' ')
#
# print('\n' + str(solve_time))
