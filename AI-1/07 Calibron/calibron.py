import sys

# CAPS =  HEIGHT FIRST
# LOWERCASE = WIDTH FIRST


def main():
    make_globals()
    checks()
    solution = backtrack("*" * (puzzle_height * puzzle_width))
    analyze(solution)


def make_globals():
    global puzzle, puzzle_height, puzzle_width, rectangles, rect_dict
    # puzzle = sys.argv[1].split()
    puzzle = "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4".split()
    puzzle_height, puzzle_width = int(puzzle[0]), int(puzzle[1])
    rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
    rect_dict = {}
    for i in range(65, 65 + len(rectangles)):
        rect_dict[chr(i)] = rectangles[i - 65]
        rect_dict[chr(i + 32)] = tuple(reversed(rectangles[i-65]))


def checks():
    global puzzle, puzzle_height, puzzle_width, rectangles, rect_dict
    areas = 0 + sum([rectangle[0] * rectangle[1] for rectangle in rectangles])
    if areas == puzzle_width * puzzle_height:
        return
    else:
        print("Containing rectangle incorrectly sized.")
        quit()


def get_possible_rectangles(board, next_spot):
    global puzzle, puzzle_height, puzzle_width, rectangles, rect_dict
    next_spot_row, next_spot_col = (next_spot // puzzle_width, next_spot % puzzle_width)
    for rect in rect_dict:
        for row in range(next_spot_row, next_spot_row + rect_dict[rect][0]):
            board_index_row = (puzzle_width * row) + next_spot_col
            print(board[board_index_row: board_index_row + rect_dict[rect][1]])


def assign(board):
    pass


def backtrack(board):
    global puzzle, puzzle_height, puzzle_width, rectangles, rect_dict
    if '*' not in board:
        return board

    next_spot = board.find('*')

    for i in get_possible_rectangles(board, next_spot):
        new_state = assign(board)
        ret = backtrack(new_state)
        if ret is not None:
            return ret

    return None


def analyze(board):
    x = 1


main()


# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output one line for each rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.
