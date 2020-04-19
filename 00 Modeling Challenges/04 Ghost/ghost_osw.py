import sys
import os

# Make a second min method
#

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

alphabet_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def word_relations(dict_txt, min_length):
    # len_to_words = {}
    all_words = set()
    all_possible_interwords = set()
    with open(dict_txt) as words_text:
        for word in words_text:
            word = word.replace('\n', '').lower()
            if str.isalpha(word) and len(word) >= min_length:
                all_words.add(word)
                all_possible_interwords.add(word)
                for i in range(1, len(word)):
                    all_possible_interwords.add(word[0:i])

    return all_words, all_possible_interwords


def main(dict_txt, min_length, current_game=None):
    global all_possible_interwords, min_length_global, all_words
    min_length_global = min_length
    all_words, all_possible_interwords = word_relations(dict_txt, min_length)

    current_game = current_game.lower() if current_game else ''

    good_results = []
    for letter in alphabet_letters:
        if valid_word(current_game + letter):
            result = minimize(current_game + letter)
            if result == 1:
                good_results.append(letter)

    if good_results:
        print("Next player can win with any of these letters: ", end='')
        print(good_results)
    else:
        print("Next player will lose!")


def maximize(word):
    global all_words

    if goal(word) is True:
        return 1

    max_value = -1

    for letter in alphabet_letters:
        new_word = word + letter
        if valid_word(new_word):
            value = minimize(new_word)
            max_value = max(max_value, value)

    return max_value


def minimize(word):
    global all_words
    # print(word)

    if goal(word) is True:
        return -1

    min_value = 1

    for letter in alphabet_letters:
        for letter2 in alphabet_letters:
            new_word = word + letter + letter2
            if valid_word(new_word):
                value = maximize(new_word)
                min_value = min(min_value, value)

    return min_value

def minimize2(word):
    global all_words
    # print(word)

    if goal(word) is True:
        return -1

    min_value = 1

    for letter in alphabet_letters:
        new_word = word + letter
        if valid_word(new_word):
            value = maximize(new_word)
            min_value = min(min_value, value)

    return min_value


def valid_word(word):
    global all_possible_interwords
    if word in all_possible_interwords:
        return True
    else:
        return False


def goal(word):
    global all_words, min_length_global
    if len(word) >= min_length_global and word in all_words:
        return True
    else:
        return False


if len(sys.argv) == 3:
    main(sys.argv[1], int(sys.argv[2]))
else:
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
# main('words_all.txt', 3, 'abec')
