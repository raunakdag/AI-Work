# Raunak Daga
# Mr. Eckel 5th PD AI
# N-Queens

import random
import collections
import time


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


def csp_backtracking(state):
    if test_solution(state):
        return state  # Testing

    threatened_queen = get_threatened_queen(state)

    if threatened_queen != -1:
        # print(threatened_queen)
        for val in get_min_conflicts(state, threatened_queen):
            new_state = state.copy()
            new_state[threatened_queen] = val
            result = csp_backtracking(new_state)
            if result is not None:
                return result
        return None


def algorithm(state):
    threatened_queen = get_threatened_queen(state)
    while(threatened_queen is not None):
        # print(get_total_conflicts(state))
        state[threatened_queen] = get_min_conflicts(state, threatened_queen)
        threatened_queen = get_threatened_queen(state)
    return state


def get_threatened_queen(state):
    # print(state)
    seen_rows = set()
    for queen_column in state:
        if state.count(queen_column) > 1:
            all_indices = [i for i, val in enumerate(state) if val == queen_column]
            seen_rows = seen_rows.union(set(all_indices))

    seen_diagonals = set()
    for queen_column in range(len(state)):  # One to check if threatened
        for queen_compare in range(queen_column + 1, len(state)):  # One to check that IS threatening
            # if state[queen_compare] - (queen_compare - queen_column) == state[queen_column]:
            #     seen_diagonals.add(queen_column)
            #     seen_diagonals.add(queen_compare)
            if abs(queen_compare - queen_column) == abs(state[queen_compare] - state[queen_column]):
                seen_diagonals.add(queen_column)
                seen_diagonals.add(queen_compare)

    # print(seen_rows.union(seen_diagonals))

    if seen_diagonals or seen_rows:
        return random.choice(tuple(seen_rows.union(seen_diagonals)))

    return None


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

    # print(least_conflict_column)

    min_value = min(least_conflict_column)
    all_min_indexes = []

    for i in range(len(least_conflict_column)):
        if least_conflict_column[i] == min_value:
            all_min_indexes.append(i)

    return random.choice(all_min_indexes)


def get_total_conflicts(state):

    least_conflict_column = [0 for x in range(len(state))]

    # Column Conflicts
    for column in range(len(state)):
        least_conflict_column[column] += (state.count(column))

    # Diagonal Conflicts
    for threatened_queen_row in range(len(state)):
        for column_moving_to in range(len(state)):  # 0, 1, 2, 3
            for queen_compare in range(len(state)):  # 1, 2, 3, 4
                if abs(queen_compare - threatened_queen_row) == abs(state[queen_compare] - column_moving_to):
                    least_conflict_column[column_moving_to] += 1

    for threatened_queen_row in range(len(state)):
        least_conflict_column[state[threatened_queen_row]] -= 2

    # print(least_conflict_column)

    return sum(least_conflict_column)


def main(num):
    # The array generated is num rows long and each value is the column it is at
    result = None
    while result is None:
        state = [random.randint(0, num-1) for i in range(num)]
        print(get_total_conflicts(state))
        result = algorithm([random.randint(0, num-1) for i in range(num)])

    # print(result)
    print(test_solution(result))


for i in range(8, 100):
    main(i)
