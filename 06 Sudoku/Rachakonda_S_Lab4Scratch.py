# Name: Sahiti Rachakonda
# Period: 4
import sys
import time
import os

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def setGlobals(puzzle):
    global size
    global N
    global height
    global width
    global setVar

    size = int(len(puzzle))  # 81

    N = int(size ** 0.5)  # 9

    sqrtN = int(N ** 0.5)  # 3

    for k in range(sqrtN, 0, -1):
        if N % k == 0:
            height = k
            width = N // height
            break

    set9 = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    setC = {"A", "B", "C"}
    setF = {"A", "B", "C", "D", "E", "F"}

    if(N == 9):
        setVar = set9
    if (N == 12):
        setVar = set9.union(setC)
    if (N == 16):
        setVar = set9.union(setF)

        # print(setVar)


def make_table_9():
    global size
    global N
    global height
    global width
    global setVar

    linear_list = [a for a in range(N * N)]
    each_row = [[x + i * 9 for x in range(N)] for i in range(N)]
    each_col = [linear_list[col::N] for col in range(N)]

    each_square = [[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26], [27, 28, 29, 36, 37, 38, 45, 46, 47], [
        30, 31, 32, 39, 40, 41, 48, 49, 50], [33, 34, 35, 42, 43, 44, 51, 52, 53], [54, 55, 56, 63, 64, 65, 72, 73, 74], [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]
    # print (each_row)
    # print(each_col)

    adjacents = {}
    adjList = each_row + each_col + each_square
    for region in adjList:
        for n1 in region:
            for n2 in region:
                if n1 != n2:
                    if n1 in adjacents:
                        adjacents[n1].add(n2)
                    else:
                        adjacents[n1] = {n2}

                    if n2 in adjacents:
                        adjacents[n2].add(n1)
                    else:
                        adjacents[n2] = {n1}

    return adjacents


def make_variables(pzl, csp_table):
    global size
    global setVar

    variables = {}
    for i in range(size):
        if pzl[i] == ".":
            variables[i] = setVar
        else:
            variables[i] = set(pzl[i])

    for ind in variables.keys():
        if len(variables[ind]) == 1:
            updateVar(variables, csp_table, ind, variables[ind])

    return variables


def updateVar(assignment, adjs, var, val):

    for adj in adjs[var]:
        assignment[adj].discard(val)

    return assignment


def updateVars(assignment, adjs, var, val):
    new_assignment = assignment.copy()

    for adj in adjs[var]:
        new_assignment[adj].discard(val)

    new_assignment[var] = {val}

    return new_assignment


def backtracking_search(assignment, adjs):
    return recursive_backtracking(assignment, adjs)


def recursive_backtracking(assignment, adjs):

    if check_complete(assignment):
        return assignment
    var = select_unassigned_var(assignment)

    for val in assignment[var]:
        if isValid(val, var, assignment, adjs):
            new_assignment = dict(assignment)
            # temp = assignment[var]
            new_assignment1 = updateVars(new_assignment, adjs, var, val)

            result = recursive_backtracking(new_assignment1, adjs)

            if result != None:
                return result

            # assignment[var] = temp

    return None


def isValid(val, var, assignment, adjs):
    for adj in adjs[var]:
        if len(assignment[adj]) == 1 and assignment[adj] == {val}:
            return False
    return True


def check_complete(assignment):
    for index in assignment.keys():
        if len(assignment[index]) != 1:
            return False

    return True


def select_unassigned_var(assignment):
    maxVal = 999999999
    maxInd = 0
    for index in assignment.keys():
        if len(assignment[index]) != 1 and len(assignment[index]) < maxVal:
            maxInd = index
            maxVal = len(assignment[index])

    return maxInd


def main():
    global size
    global N

    sysfinal = time.time()

    index = 1
    filename = "sudoku_puzzles_1.txt"

    with open(filename) as file:
        for puzzle in file:
            puzzle = puzzle.replace("\n", "").strip()
            setGlobals(puzzle)
            csp_table_9 = make_table_9()

            # print(csp_table_9)

            variables = make_variables(puzzle, csp_table_9)

            solution = backtracking_search(variables, csp_table_9)

            puzzleString = ""
            ascii_sum = 0
            for ind in range(size):
                l = solution[ind].pop()
                puzzleString += l
                ascii_sum += ord(l)
            ascii_sum -= 48 * N ** 2

            # print(index, ":", time.time() - sysfinal)
            # print("     (", ascii_sum, ":", puzzleString, ")")

            index += 1


if __name__ == '__main__':
    main()
