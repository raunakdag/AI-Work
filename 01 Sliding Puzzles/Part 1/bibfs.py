import os
import collections
import time
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def print_puzzle(state, size):
    for i in range(0, len(state), int(size)):
        print(" ".join(state[i: i + int(size)]))


def find_goal(state):
    return(''.join(sorted(state.replace('.', '')))+".")


def swap_characters(s, i1, i2):
    stringList = list(s)
    stringList[i1], stringList[i2] = stringList[i2], stringList[i1]
    return "".join(stringList)


def get_children(state, size):
    boards = []
    index = state.index('.')

    if ((index) % int(size)) != 0:
        boards.append(swap_characters(state, index, index - 1))
    if ((index + 1) % int(size)) != 0:
        boards.append(swap_characters(state, index, index + 1))
    if (index + int(size) < len(state)):
        boards.append(swap_characters(state, index, index + int(size)))
    if (index - int(size) > -1):
        boards.append(swap_characters(state, index, index - int(size)))

    return boards


def bfs_shortest_path(board_state, size):
    fringe = collections.deque()
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    goal_state = find_goal(board_state).replace('\n', '')
    while(fringe):
        current = fringe.pop()
        if(current == goal_state):
            steps = path(current, parents, size)
            steps.insert(0, board_state.replace('\n', ''))
            return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return None


def bibfs(board_state, size):
    board_state = board_state.replace('\n', '')
    goal_state = find_goal(board_state).replace('\n', '')

    fringe_front, fringe_back = collections.deque(), collections.deque()
    visited_front, visited_back = set(), set()
    parents_front, parents_back = {board_state: "start"}, {goal_state: "start"}

    fringe_front.append(board_state)
    visited_front.add(board_state)

    fringe_back.append(goal_state)
    visited_back.add(goal_state)

    while fringe_front and fringe_back:
        current_front, current_back = fringe_front.pop(), fringe_back.pop()
        if(current_front == goal_state):
            steps = path(current_front, parents_front, size)
            steps.insert(0, board_state.replace('\n', ''))
            return steps

        for board in get_children(current_front, size):
            if board not in visited_front:
                fringe_front.appendleft(board)
                visited_front.add(board)
                if board != board_state:
                    parents_front[board] = current_front
                if board in fringe_back:
                    steps = path(current_front, parents_front, size)
                    steps.insert(0, board_state)
                    steps_back = path(board, parents_back, size)[::-1]
                    steps.extend(steps_back)
                    steps.append(goal_state)
                    return steps

        for board in get_children(current_back, size):
            if board not in visited_back:
                fringe_back.appendleft(board)
                visited_back.add(board)
                parents_back[board] = current_back
                if board in fringe_front:
                    steps = path(board, parents_front, size)
                    steps.insert(0, board_state)
                    steps_back = path(current_back, parents_back, size)[::-1]
                    steps.extend(steps_back)
                    steps.append(goal_state)
                    return steps

    return None


def path(board_state, parents, size):

    listmoves = []
    while parents[board_state] != "start":
        # print(board_state)
        # print(parents)
        listmoves.append(board_state)
        board_state = parents[board_state]
    listmoves = listmoves[::-1]
    return listmoves


def compare(filename):
    with open(filename) as f:
        puzzle_number = 1
        for line in f:
            size = line[0:1]
            puzzle = line[2:]
            start = time.perf_counter()
            steps = bfs_shortest_path(puzzle, size)
            end = time.perf_counter()
            print("Time For Bfs " + str(puzzle_number) +
                  ": " + str(end-start) + " in " + str(len(steps)) + " moves")
            start = time.perf_counter()
            steps = bibfs(puzzle, size)
            end = time.perf_counter()
            print("Time For BiBfs " + str(puzzle_number) + ": " +
                  str(end-start) + " in " + str(len(steps)) + " moves")
            puzzle_number += 1


# filename = sys.argv[1]
filename = "slide_puzzle_tests.txt"

compare(sys.argv[1])
