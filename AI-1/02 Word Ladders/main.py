# Raunak Daga
# Mr. Eckel PD 5 AI
# Word Ladders
import sys
import os
import pickle
import collections
import time
# file1, file2 = sys.argv[1], sys.argv[2]

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def find_words(words_file):
    start = time.perf_counter()
    pairs = {}
    all_words = []
    with open(words_file) as words_text:
        for word in words_text:
            all_words.append(word.replace('\n', ''))

    # print(all_words)

    for word in all_words:
        pairs[word] = []
        for word_match in all_words:
            if letters_away(word, word_match):
                pairs[word].append(word_match)
    end = time.perf_counter()
    print("The time to create the data structure was: " + str(end-start))
    print("There are " + str(len(all_words)) + " words in this dict.")
    print()
    return pairs


def letters_away(first, second):
    num_different_chars = sum(1 for pos in range(len(first)) if first[pos] != second[pos])
    return num_different_chars == 1


def smallest_distance(first, second, word_relations):
    fringe = collections.deque()
    visited = set()

    parents = {
        first: "start"
    }

    fringe.append(first)
    visited.add(first)

    while(fringe):
        current = fringe.pop()
        if(current == second):
            listwords = path(current, parents)
            listwords.insert(0, first)
            return listwords
        for parent_word in word_relations[current]:
            if parent_word not in visited:
                fringe.appendleft(parent_word)
                visited.add(parent_word)
                parents[parent_word] = current

    return None


def path(endword, parents):
    listwords = []
    while parents[endword] != "start":
        listwords.append(endword)
        endword = parents[endword]
    listwords = listwords[::-1]
    return listwords

# word_relations = find_words()
# with open("data.pkl", "wb") as outfile:
#     pickle.dump(word_relations, outfile)


# word_relations = 'temp'
# with open("data.pkl", "rb") as infile:
#     word_relations = pickle.load(infile)

words_file, puzzles_file = sys.argv[1], sys.argv[2]
word_relations = find_words(words_file)
with open(puzzles_file) as puzzles:
    count = 0
    startTime = time.perf_counter()
    for puzzle in puzzles:
        start, end = puzzle.split()[0], puzzle.split()[1]
        words = smallest_distance(start, end, word_relations)
        print("Line: " + str(count))
        if words:
            print("Length is: " + str(len(words)))
            for link in smallest_distance(start, end, word_relations):
                print(link)
        else:
            print("No solution!")
        print()
        count += 1
    end = time.perf_counter()
    print("Time to solve all of these puzzles was: " + str(end-startTime))
