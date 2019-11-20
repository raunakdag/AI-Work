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

# nodes_bfs, nodes_dfs, nodes_iddfs, nodes_astar = (0, 0, 0, 0)

global nodes_bfs
global nodes_dfs
global nodes_iddfs
global nodes_astar


def amt_puzzles():

    closed = set()
    amt = {

    }
    start_node = (1, 'ABCDEFGH.', 0)
    heap = []
    heappush(heap, start_node)

    while heap:
        current = heappop(heap)
        print(current[1] + " Depth:" + str(current[2]))
        # print(current)
        # return current[2]

        if current[1] not in closed:
            if str(current[2]) in amt:
                amt[str(current[2])] += 1
            else:
                amt[str(current[2])] = 1

            closed.add(current[1])
            for board in get_children(current[1], 3):
                heappush(heap, (1, board, current[2] + 1))

    print(amt)
    return None


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
            return nodes_bfs
            # steps = path(current, parents, size)
            #
            # return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return nodes_bfs


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


def dfs_shortest_path(board_state, size):
    fringe = []
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    nodes_dfs = 0
    goal_state = find_goal(board_state).replace('\n', '')
    while(fringe):
        nodes_dfs += 1
        current = fringe.pop()
        # print(current)
        if(current == goal_state):
            return nodes_dfs
            # steps = dfs_path(current, parents, size)
            #
            # return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.append(board)
                visited.add(board)
                parents[board] = current

    return nodes_dfs


def dfs_path(board_state, parents, size):
    listmoves = []
    while parents[board_state] != "start":
        # print('made it to end)' + parents[board_state])
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


def kDFS(board_state, size, k):
    goal = find_goal(board_state.replace("\n", ""))

    start_node = (board_state.replace("\n", ""), 0, {board_state}, [board_state])
    fringe = []
    fringe.append(start_node)

    parents = {
        board_state.replace('\n', ''): "start"
    }

    nodes_iddfs = 0
    while(fringe):
        current = fringe.pop()
        nodes_iddfs += 1
        # print(str(current) + " Steps: " + str(current[3]))
        if(current[0] == goal):
            # steps = dfs_path(current[0], parents, size)
            return nodes_iddfs
            # return current[1]
        if current[1] < k:
            for board in get_children(current[0], size):
                # print(str(board) + " " + str(current[2]))
                if board not in current[2]:
                    temp_set = {board}
                    unionized_set = current[2].union(temp_set)

                    temp_list = current[3]
                    temp_list.append(current[0])
                    fringe.append((board, current[1] + 1, unionized_set, temp_list))
                    if board not in parents:
                        parents[board] = current[0]

    return nodes_iddfs


def id_dfs(board_state, size):
    path = None
    k = 0
    while path is None:
        path = kDFS(board_state, size, k)
        # print(str(k) + str(path))
        k += 1

    return path


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


def a_star(board_state, size):
    goal = find_goal(board_state.replace("\n", ""))

    closed = set()
    parents = {
        board_state.replace('\n', ''): "start"
    }

    start_node = (a_star_heuristic(board_state, size), board_state, 0)
    heap = []
    heappush(heap, start_node)

    nodes_astar = 0
    while heap:
        current = heappop(heap)
        nodes_astar += 1
        # print(current)
        if current[1] == goal:
            # print('made it to goal')
            # steps = dfs_path(current[1], parents, size)
            return nodes_astar
            # return current[2]

        if current[1] not in closed:
            closed.add(current[1])
            for board in get_children(current[1], size):
                heappush(heap, (current[2] + a_star_heuristic(board, size), board, current[2] + 1))
                if board not in parents:
                    parents[board] = current[1]

    return nodes_astar


def a_star_heuristic(board_state, size):
    goal = find_goal(board_state.replace("\n", ""))
    inversions = 0
    for letter in board_state:
        if letter != '.':
            total_inv = abs((board_state.find(letter) // size) - (goal.find(letter) // size))
            total_inv += abs((board_state.find(letter) % size) - (goal.find(letter) % size))
            inversions += total_inv

    return inversions


def main():
    filename = 'slide_puzzle_tests_2.txt'
    # filename = sys.argv[1]
    with open(filename) as puzzles:
        count = 0
        startTime = time.perf_counter()
        for puzzle in puzzles:
            size_string, board_state, type = puzzle.split()[0], puzzle.split()[1], puzzle.split()[2]

            size = int(size_string)
            do_puzzles = True

            parity_start = time.perf_counter()
            do_puzzles = parity_check(board_state, size)
            parity_end = time.perf_counter()

            if do_puzzles:
                if type == 'I':
                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", ID-DFS - " + str((id_dfs(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

                elif type == 'B':
                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", BFS - " + str(len(bfs_shortest_path(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

                elif type == 'A':
                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", A* - " + str((a_star(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

                elif type == '!':
                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", ID-DFS - " + str((id_dfs(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", BFS - " + str(len(bfs_shortest_path(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

                    startTime = time.perf_counter()
                    print("Line: " + str(count) + " " + board_state +
                          ", A* - " + str((a_star(board_state, size))), end="")
                    end = time.perf_counter()
                    print(" moves in " + str(end-startTime) + " seconds")

            else:
                print("Line: " + str(count) + " " + board_state +
                      ", no solution determined in " + str(parity_end - parity_start) + " seconds")

            print()
            count += 1

# EXTENSION D


def extension_d():
    startBFS = time.perf_counter()
    nodes_bfs = bfs_shortest_path('AIBCFOGD.EKHMJNL', 4)
    endBFS = time.perf_counter()
    print('BFS done')

    startDFS = time.perf_counter()
    nodes_dfs = dfs_shortest_path('.25187643', 3)
    endDFS = time.perf_counter()
    print('BFS done')

    startIDDFS = time.perf_counter()
    nodes_iddfs = id_dfs('EICDJGLHBAK.NMOF', 4)
    endIDDFS = time.perf_counter()
    print('BFS done')

    startASTAR = time.perf_counter()
    nodes_astar = a_star('EICDJGLHBAK.NMOF', 4)
    endASTAR = time.perf_counter()
    print('BFS done')

    print('Puzzle: AIBCFOGD.EKHMJNL')
    print('Amount of nodes processed by BFS per second: ' + str(nodes_bfs / (endBFS - startBFS)))
    print('Amount of nodes processed by DFS per second: ' + str(nodes_dfs / (endDFS - startDFS)))
    print('Amount of nodes processed by ID-DFS per second: ' +
          str(nodes_iddfs / (endIDDFS - startIDDFS)))
    print('Amount of nodes processed by A* per second: ' +
          str(nodes_astar / (endASTAR - startASTAR)))


# EXTENSION E
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


# extension_e_5()
# print(bfs_shortest_path('ABNCDFGHIEKL.MJPQRSOUVWXT', 5))
