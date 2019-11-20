# Raunak Daga
# Mr. Eckel 5th PD AI
# Sliding Puzzles

import os
import collections
import sys
import time

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

    # To the left
    if ((index) % int(size)) != 0:
        boards.append(swap_characters(state, index, index - 1))

    # To the right
    if ((index + 1) % int(size)) != 0:
        boards.append(swap_characters(state, index, index + 1))

    # Swap . with down
    if (index + int(size) < len(state)):
        boards.append(swap_characters(state, index, index + int(size)))

    # Swap . with up
    if (index - int(size) > -1):
        boards.append(swap_characters(state, index, index - int(size)))

    return boards


def bfs_iterative(goal_state, size):
    fringe = collections.deque()
    visited = set()
    fringe.append(goal_state.replace('\n', ''))
    visited.add(goal_state.replace('\n', ''))
    count = 0
    while(fringe):
        current = fringe.pop()
        count += 1
        for board in get_children(current, size):
            if board not in visited:
                board = board.replace('\n', '')
                fringe.append(board)
                visited.add(board)

    return count


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


def path(board_state, parents, size):
    listmoves = []
    while parents[board_state] != "start":
        listmoves.append(board_state)
        board_state = parents[board_state]
    listmoves = listmoves[::-1]
    # for move in listmoves:
    #     print_puzzle(move, size)
    #     print()
    return listmoves


def hardest_puzzle():
    start_state = '12345678.'
    size = 3

    fringe = collections.deque()
    visited = set()

    fringe.append(start_state.replace('\n', ''))
    visited.add(start_state.replace('\n', ''))

    lastOne = start_state
    lastTwo = start_state
    while(fringe):
        current = fringe.pop()
        for board in get_children(current, size):
            if board not in visited:
                lastTwo = lastOne
                lastOne = board
                fringe.appendleft(board)
                visited.add(board)

    bfs_shortest_path(lastOne, 3)
    bfs_shortest_path(lastTwo, 3)
    print("Length: " + str(len(bfs_shortest_path(lastOne, 3))-1))


def do_tasks(filename):
    with open(filename) as f:
        puzzle_number = 0
        for line in f:
            size = line[0:1]
            puzzle = line[2:].replace('\n', '')

            start = time.perf_counter()
            solution_length = (len(bfs_shortest_path(puzzle, size))-1)
            end = time.perf_counter()

            print("Line " + str(puzzle_number) + ": " + puzzle + ", " + str(solution_length) +
                  " moves found in " + str(end - start) + " seconds")

            puzzle_number += 1


filename = sys.argv[1]
do_tasks(filename)
