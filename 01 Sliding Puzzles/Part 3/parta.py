# Raunak Daga
# Mr. Eckel 5th PD AI
# Sliding Puzzles Part 2

import os
import collections
import time
import heapq
from heapq import heappush, heappop
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
    while(fringe):
        current = fringe.pop()
        if(current == goal_state):
            steps = path(current, parents, size)

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


def dfs_shortest_path(board_state, size):
    fringe = []
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
            steps = dfs_path(current, parents, size)

            return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.append(board)
                visited.add(board)
                parents[board] = current

    return None


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

    while(fringe):
        current = fringe.pop()
        # print(str(current) + " Steps: " + str(current[3]))
        if(current[0] == goal):
            # steps = dfs_path(current[0], parents, size)

            return current[1]
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

    return None


def id_dfs(board_state, size):
    path = None
    k = 0
    while path is None:
        path = kDFS(board_state, size, k)
        # print(str(k) + str(path))
        k += 1

    return path


def new_a_star(board_state, size, multiplier_value):
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
        if current[1] == goal:
            return current[2]

        if current[1] not in closed:
            closed.add(current[1])
            for board in get_children(current[1], size):
                heappush(heap, (multiplier_value *
                                current[2] + a_star_heuristic(board, size), board, current[2] + 1))
                if board not in parents:
                    parents[board] = current[1]

    return None


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
    # filename = sys.argv[1]
    filename = '15_puzzles.txt'
    start_overall = time.perf_counter()
    with open(filename) as puzzles:
        count = 1
        moves = 0
        startTime = time.perf_counter()
        for puzzle in puzzles:
            size_string, board_state, type = 4, puzzle.replace('\n', ''), 'a'

            size = int(size_string)
            startTime = time.perf_counter()
            moves_astar = new_a_star(board_state, size, 0.1)
            moves += moves_astar
            print("Line: " + str(count) + " " + board_state +
                  ", A* - " + str(moves_astar), end="")
            end = time.perf_counter()
            print(" moves in " + str(end-startTime) + " seconds")

            print()
            count += 1
    end_overall = time.perf_counter()
    print(str(end_overall-start_overall))
    print(moves)


main()
