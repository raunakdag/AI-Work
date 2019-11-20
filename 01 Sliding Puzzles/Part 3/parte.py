# Raunak Daga
# Mr. Eckel 5th PD AI
# Sliding Puzzles Part 2

import os
import collections
import time
import heapq
from heapq import heappush, heappop
import sys
import random

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


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


def bfs_shortest_path(board_state, size):
    fringe = collections.deque()
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    goal_state = find_goal(board_state).replace('\n', '')
    nodes_bfs = 0
    while(fringe):
        current = fringe.pop()
        nodes_bfs += 1
        if(current == goal_state):
            # return nodes_bfs
            steps = path(current, parents, size)

            return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return nodes_bfs


def generate_puzzles(board_state, size, solution_length):
    fringe = collections.deque()
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    while(fringe):
        current = fringe.pop()

        if len(path(current, parents, size)) == solution_length:
            steps = path(current, parents, size)
            steps.append(board_state.replace('\n', ''))
            print(current)
            return steps
        boards = get_children(current, size)
        random.shuffle(boards)
        for board in boards:
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return 0


def path(board_state, parents, size):
    listmoves = []
    while parents[board_state] != "start":
        listmoves.append(board_state)
        board_state = parents[board_state]
    listmoves = listmoves[::-1]
    return listmoves


def parity_check(board_state, size_string):
    size = int(size_string)
    numInv = 0
    board = board_state.replace('.', '')

    for char in board:
        for letter_ahead in board[board.index(char)+1:]:
            if ord(letter_ahead) < ord(char):
                numInv += 1

    if size % 2 != 0:
        if numInv % 2 != 0:
            return False
        return True
    else:
        if (board_state.index('.') // size) % 2 != 0:
            if numInv % 2 == 0:
                return True
            return False
        else:
            if numInv % 2 != 0:
                return True
            return False

    return False


def a_star(board_state, size, goal_depth):
    goal = find_goal(board_state.replace("\n", ""))

    closed = set()
    parents = {
        board_state.replace('\n', ''): "start"
    }

    start_node = (a_star_heuristic(board_state, size), board_state, 0)
    heap = []
    heappush(heap, start_node)

    while heap:
        current = heappop(heap)
        if goal_depth == (31 - current[2]):
            return current[1]

        if current[1] not in closed:
            closed.add(current[1])
            boards = get_children(current[1], size)
            random.shuffle(boards)
            for board in get_children(current[1], size):
                heappush(heap, (current[2] + a_star_heuristic(board, size), board, current[2] + 1))
                if board not in parents:
                    parents[board] = current[1]

    return 0


def a_star_heuristic(board_state, size):
    goal = find_goal(board_state.replace("\n", ""))
    inversions = 0
    for letter in board_state:
        if letter != '.':
            total_inv = abs((board_state.find(letter) // size) - (goal.find(letter) // size))
            total_inv += abs((board_state.find(letter) % size) - (goal.find(letter) % size))
            inversions += total_inv

    return inversions


def extension_e_3(num):
    puzzle = ''.join(random.sample('ABCDEFGH.', len('ABCDEFGH.')))
    while(parity_check(puzzle, 3) is not True):
        puzzle = ''.join(random.sample('ABCDEFGH.', len('ABCDEFGH.')))

    for i in range(31):
        puzzle = (a_star('ABCDEFGH.', 3, i))
        print(puzzle)
        print(len(bfs_shortest_path(puzzle, 3)))

    return (a_star(puzzle, 3, num))

    # puzzle = extension_e(5)
    # print(puzzle)
    # print(len(bfs_shortest_path('FD.HEGCBA', 3)))


def extension_e_5():
    puzzle = ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWX.', 24))
    while(parity_check(puzzle, 5) is not True):
        puzzle = ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWX.', 24))

    puzzle = 'ABCDEFGHIJKLMNOPQRSTUVWX.'
    for i in range(31):
        print(len(generate_puzzles(puzzle, 5, i))-1)

    # puzzle = extension_e(5)
    # print(puzzle)
    # print(len(bfs_shortest_path('FD.HEGCBA', 3)))


extension_e_5()
# print(bfs_shortest_path('ABNCDFGHIEKL.MJPQRSOUVWXT', 5))
