# Raunak Daga
# Mr. Eckel 5th PD AI
# N-Queens

import random
import collections
import time


def test_solution(state):
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


def algorithm(state):
    threatened_queen = get_threatened_queen(state)
    while(threatened_queen is not None):
        state[threatened_queen] = get_min_conflicts(state, threatened_queen)
        threatened_queen = get_threatened_queen(state)
    return state


def get_threatened_queen(state):
    seen_rows = set()
    for queen_column in state:
        if state.count(queen_column) > 1:
            all_indices = [i for i, val in enumerate(state) if val == queen_column]
            seen_rows = seen_rows.union(set(all_indices))

    seen_diagonals = set()
    for queen_column in range(len(state)):  # One to check if threatened
        for queen_compare in range(queen_column + 1, len(state)):  # One to check that IS threatening
            if abs(queen_compare - queen_column) == abs(state[queen_compare] - state[queen_column]):
                seen_diagonals.add(queen_column)
                seen_diagonals.add(queen_compare)

    if seen_diagonals or seen_rows:
        return random.choice(tuple(seen_rows.union(seen_diagonals)))

    return None


def get_min_conflicts(state, threatened_queen_row):
    least_conflict_column = [0 for x in range(len(state))]

    for column in range(len(state)):
        least_conflict_column[column] += (state.count(column))

    for column_moving_to in range(len(state)):
        for queen_compare in range(len(state)):
            if abs(queen_compare - threatened_queen_row) == abs(state[queen_compare] - column_moving_to):
                least_conflict_column[column_moving_to] += 1

    least_conflict_column[state[threatened_queen_row]] -= 2

    min_value = min(least_conflict_column)
    all_min_indexes = []

    for i in range(len(least_conflict_column)):
        if least_conflict_column[i] == min_value:
            all_min_indexes.append(i)

    return random.choice(all_min_indexes)


def main(a, b):
    for i in range(a, b):
        result = None
        while result is None:
            state = [random.randint(0, i-1) for l in range(i)]
            result = algorithm(state)
        print(result)
        print(test_solution(result))


# main(8, 200)
result = None
while result is None:
    state = [random.randint(0, 200-1) for l in range(200)]
    result = algorithm(state)
print(result)
print(test_solution(result))
