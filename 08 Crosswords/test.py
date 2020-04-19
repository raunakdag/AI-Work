import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def make_dictionary(filename):
    global patterns, letter_count
    patterns, letter_count = {}, {}

    with open(filename) as words_text:
        for word in words_text:
            word = word.replace('\n', '').rstrip()
            word = word.lower()
            # print(word)

            len_w = len(word)
            if str.isalpha(word) and len_w >= 3:
                # All Blanks
                if '-' * len_w in patterns:
                    if len(word) >= 3:
                        patterns['-' * len_w].add(word)
                else:
                    if len(word) >= 3:
                        patterns['-' * len_w] = set(word)

                for index in range(len_w):
                    # One Blank at Each
                    p_match = place_at_index('-' * len_w, word[index], index)
                    if p_match in patterns:
                        patterns[p_match].add(word)
                    else:
                        patterns[p_match] = set([word])

                    # letter Count
                    if word[index] not in letter_count:
                        letter_count[word[index]] = 1
                    else:
                        letter_count[word[index]] += 1

        print(patterns['-t--'])

def place_at_index(string, char, index):
    return string[0: (index)] + char + string[(index) + 1:]

def main():
    global patterns
    make_dictionary('twentyk.txt')
    print(patterns['-t--'])


main()
