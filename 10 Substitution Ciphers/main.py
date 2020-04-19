import os
import random
import sys
import csv
import math
from math import log2

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LEN_S = 26

POPULATION = 500
CLONES = 1
MUTATION_RATE = 0.8
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN = .75
CROSSOVER_POINTS = 5
N_GRAM_LENGTH = 4

# Helper Methods

def shuffle_string(string):
    return ''.join(random.sample(string, len(string)))

def encode(cipher):
    global text
    return ''.join([cipher[ALPHABET.find(text[ch])] if text[ch] in ALPHABET else text[ch] for ch in range(len(text))])

def decode(cipher):
    global text
    return ''.join([ALPHABET[cipher.find(text[ch])] if text[ch] in ALPHABET else text[ch] for ch in range(len(text))])

def get_ngrams(string, n_gram=4):
    return[word[i: i + n_gram] for word in string.split()
           for i in range(len(word)) if len(word) >= n_gram and len(word[i: i + n_gram]) >= n_gram]

def swap_characters(string, i, j):
    lst = list(string)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def make_scores(population):
    return {pop_piece: fitness(pop_piece) for pop_piece in population}

# Algorithm Methods
def make_clones(scores):
    best_clone = 0
    current_max = -100
    for i in scores:
        if scores[i] > current_max:
            best_clone = i
            current_max = scores[i]
    return [best_clone]


def fitness(cipher):
    global n_grams_to_frequency, text
    n_grams = get_ngrams(decode(cipher), n_gram=N_GRAM_LENGTH)
    return sum([log2(n_grams_to_frequency[gram]) for gram in n_grams if gram in n_grams_to_frequency])


def selection(strategies, scores):
    strats = list(random.sample(strategies, TOURNAMENT_SIZE * 2))
    tournament1 = strats[0: TOURNAMENT_SIZE]
    tournament2 = strats[TOURNAMENT_SIZE:]

    list.sort(tournament1, key=lambda strat: scores[strat], reverse=True)
    list.sort(tournament2, key=lambda strat: scores[strat], reverse=True)

    strat1 = None
    strat2 = None

    s1_count = 0
    while strat1 is None:
        if random.random() < TOURNAMENT_WIN:
            strat1 = tournament1[s1_count]
        s1_count += 1

    s2_count = 0
    while strat2 is None:
        if random.random() < TOURNAMENT_WIN:
            strat2 = tournament2[s2_count]
        s2_count += 1

    return strat1, strat2


def breed(strategy1, strategy2):
    list_locs = random.sample(range(0, len(strategy1)), CROSSOVER_POINTS)
    new_strat = '-' * len(strategy1)

    for loc in list_locs:
        new_strat = new_strat[0: loc] + strategy1[loc] + new_strat[loc + 1:]

    for ch in strategy2:
        if ch not in new_strat and new_strat.find('-') != -1:
            ind = new_strat.find('-')
            new_strat = new_strat[0: ind] + ch + new_strat[ind + 1:]

    if random.random() < MUTATION_RATE:
        new_strat = swap_characters(
            new_strat, *random.sample(range(0, len(strategy1)), 2))

    return new_strat


def main(text_var):
    global text, n_grams_to_frequency
    text = text_var.upper()

    n_grams_to_frequency = {}
    with open('ngrams1.tsv') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for row in tsvreader:
            if len(row[0]) == N_GRAM_LENGTH:
                n_grams_to_frequency[row[0]] = int(row[1])

    # print(fitness(shuffle_string(ALPHABET)))

    current_pop = [shuffle_string(ALPHABET) for i in range(POPULATION)]

    gen = 0
    while True:
        scores = make_scores(current_pop)
        new_pop = [current_pop[0]]
        # print(str(gen) + ": " + decode(new_pop[0]))
        # new_pop = []
        while len(new_pop) != POPULATION:
            new_strat = breed(*selection(current_pop, scores))
            if new_strat not in new_pop:
                new_pop.append(new_strat)
        list.sort(new_pop, key=lambda strat: fitness(strat), reverse=True)
        # print(fitness(new_pop[0]))
        print(str(gen) + ": " + decode(new_pop[0]))
        gen += 1
        current_pop = new_pop


main(sys.argv[1])
# print(breed('ABCDEFGHIJKLMNOPQRSTUVWXYZ', shuffle_string(ALPHABET)))
