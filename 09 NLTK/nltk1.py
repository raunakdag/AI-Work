import nltk
# from nltk.book import *
from nltk import FreqDist
from nltk.corpus import stopwords,brown
from nltk.corpus import state_union
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from urllib import request
from bs4 import BeautifulSoup
from nltk.corpus import movie_reviews

# 2)	In Chapter 2, complete exercises 4, 5, 7, 9, 12, 17, 18, 23, and 27.
# 3)	In Chapter 3, complete exercises 20 and 22.
# 4)	In Chapter 6, complete exercise 4.



def chapter2_exercise4():
    # Read in the texts of the State of the Union addresses, using the state_union corpus reader.Count occurrences of
    # men, women, and people in each document.What has happened to the usage of these words over time?
    files = state_union.fileids()
    men = dict()
    women = dict()
    people = dict()
    for index, file in enumerate(files):
        words = sorted(state_union.words(fileids=[file]))
        men[file] = words.count("men")
        women[file] = words.count("women")
        people[file] = words.count("people")
        print(file[:4], men[file], women[file], people[file], end="      ")
        if index % 6 == 5:
            print()
    print("\nMEN")
    for file, men_c in men.items():
        print(file[:4], men_c)
    print("\nWOMEN")
    for file, women_c in women.items():
        print(file[:4], women_c)
    print("\nPERSON")
    for file, person_c in people.items():
        print(file[:4], person_c)
    print("men:", sum(men.values()))
    print("women:", sum(women.values()))
    print("people:", sum(people.values()))


def helper2_5(word):
    print(word.upper())
    print("Member Meronyms:", [synset3.name() for synset3 in wn.synset(word).member_meronyms()])
    print("Part Meronyms:", [synset1.name() for synset1 in wn.synset(word).part_meronyms()])
    print("Substance Meronyms:", [synset2.name() for synset2 in wn.synset(word).substance_meronyms()])
    print("Member Holonyms:", [synset6.name() for synset6 in wn.synset(word).member_holonyms()])
    print("Part Holonyms:", [synset4.name() for synset4 in wn.synset(word).part_holonyms()])
    print("Substance Holonyms:", [synset5.name() for synset5 in wn.synset(word).substance_holonyms()])
    print()


def chapter2_exercise5():
    # Investigate the holonym - meronym relations for some nouns.Remember that there are three kinds of
    # holonym-meronym relation, so you need to use: member_meronyms(), part_meronyms(), substance_meronyms(),
    # member_holonyms(), part_holonyms(), and substance_holonyms().
    helper2_5('meat.n.01')
    helper2_5('plant.n.02')
    helper2_5('pencil.n.01')
    helper2_5('egg.n.01')
    helper2_5('dog.n.01')
    helper2_5('doorknob.n.01')
    helper2_5('rock.n.02')


def chapter2_exercise7():
    # According to Strunk and White's Elements of Style, the word however, used at the start of a sentence,
    # means "in whatever way" or "to whatever extent", and not "nevertheless". They give this example of correct usage:
    # However you advise him, he will probably do as he thinks best. (http://www.bartleby.com/141/strunk3.html) Use the
    # concordance tool to study actual usage of this word in the various texts we have been considering. See also the
    # LanguageLog posting "Fossilized prejudices about 'however'" at http://itre.cis.upenn.edu/~myl/languagelog/archives/001913.html
    # emma = brown.words('austen-emma.txt')
    category = ['adventure', 'belles_lettres', 'editorial', 'fiction', 'government', 'hobbies', 'humor', 'learned',
                'lore', 'mystery', 'news', 'religion', 'romance', 'science_fiction']
    emma = nltk.Text(brown.words(categories=category))
    emma.concordance("however", width=85, lines=32)


def chapter2_exercise9():
    # Pick a pair of texts and study the differences between them, in terms of vocabulary, vocabulary richness, genre,
    # etc. Can you find pairs of words that which have quite different meanings across the two texts?
    # print(brown.categories())
    # print(brown.fileids())
    # print(brown.words(categories=['mystery']))
    # print(brown.words(fileids=['cl13']))
    # print(set(text1))
    count = dict()
    for word in list(text1):
        if word.isalpha():
            if word.upper() in count:
                count[word.upper()] += 1
            else:
                count[word.upper()] = 1
    # print(count)
    # print(sorted(count, key=count.get,reverse=True))
    # sorted(d, key=d.get, reverse=True)
    # print("\n\n\n\n")
    print({k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True) if v > 100})
    # count = dict()
    for word in list(text9):
        if word.isalpha():
            if word.upper() in count:
                count[word.upper()] += 1
            else:
                count[word.upper()] = 1
    # print(count)
    # print(sorted(count, key=count.get,reverse=True))
    # sorted(d, key=d.get, reverse=True)
    print("\n\n\n\n")
    print({k.lower(): v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True) if v > 100})
    # print(set(text2))
    common = "white"
    print("1")
    text1.concordance(common, lines=10)
    print("2")
    text2.concordance(common, lines=10)


def chapter2_exercise17():
    stopwords = stopwords.words("english")
    top_50 = FreqDist(brown.words(categories='romance'))
    temp = top_50.copy()
    for word in temp:
        if word in top_50 and word in stopwords:
            top_50.pop(word)
    return top_50.most_common(50)


def chapter2_exercise18():
    freq_dist = FreqDist(brown.words(categories='humor'))
    stopwords_list = stopwords.words("english")
    for word in freq_dist.copy():
        if word in freq_dist and (not word.isalpha() or word in stopwords_list):
            freq_dist.pop(word)
    bigrams_dist = FreqDist([(item1, item2) for item1, item2 in nltk.bigrams(brown.words(categories='humor'))
                             if item1 in freq_dist and item2 in freq_dist])
    return bigrams_dist.most_common(50)


def chapter3_exercise20():
    url = "https://www.reddit.com/r/globaloffensive"
    raw_text = BeautifulSoup(request.urlopen(url_string).read().decode('utf8'), 'html.parser').get_text()
    text = nltk.Text(nltk.word_tokenize(raw_text)[:1000])
    text.concordance('the')


all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)#[:2000][1]


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


def chapter6_exercise4():
    documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    featuresets = [(document_features(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[50:], featuresets[:50]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(classifier.show_most_informative_features(30))



# chapter2_exercise4()
# chapter2_exercise5()
# chapter2_exercise7()
# chapter2_exercise9()
# chapter3_exercise20()
chapter6_exercise4()
