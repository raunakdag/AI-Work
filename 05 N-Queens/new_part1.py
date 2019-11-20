# Raunak Daga
# Mr. Eckel 5th PD AI
# N-Queens


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
    # print(state)
    if test_solution(state):
        return state
    var = get_next_unassigned_var(state)
    if var != -1:
        for val in get_sorted_values(state, var):
            new_state = state.copy()
            new_state[var] = val
            result = csp_backtracking(new_state)
            if result is not None:
                return result
        return None


def get_next_unassigned_var(state):
    try:
        return state.index(-1)
    except:
        return -1


def get_sorted_values(state, var):
    available_locations = []

    for column in range(len(state)):
        if state.count(column) == 0:
            available_locations.append(column)

    for column_moving_to in range(len(state)):  # 0, 1, 2, 3
        for queen_compare in range(len(state)):  # 1, 2, 3, 4
            if abs(queen_compare - var) == abs(state[queen_compare] - column_moving_to):
                least_conflict_column[column_moving_to] += 1

    return(available_locations)


def main():
    result = csp_backtracking([-1 for i in range(11)])
    print(result)
