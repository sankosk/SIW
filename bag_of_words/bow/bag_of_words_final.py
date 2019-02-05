#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import argparse, nltk
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

"""
Author:         Esteban Montes, UO246305
Description:    Tarea 3 - bag o words
References:     Bird, Steven, Edward Loper and Ewan Klein (2009),
                Natural Language Processing with Python. O’Reilly Media Inc.
"""

""" REQUIREMENTS
nltk.download('punkt')
nltk.download('stopwords')
"""

"""
COEFICIENTS
"""
coef_dice           =       lambda b1, b2: 2 * len(b1.intersection(b2)) / (len(b1) + len(b2))
coef_jaccard        =       lambda b1, b2: len(b1.intersection(b2)) / len(b1.union(b2))
coef_cosine         =       lambda b1, b2: len(b1.intersection(b2)) / (len(b1) * len(b2))
coef_overlapping    =       lambda b1, b2: len(b1.intersection(b2)) / min(len(b1), len(b2))


def string_to_bag_of_words(text):
    return Counter(text)

class SimilarityChecker:

    def __init__(self, queries, texts):
        self.queries, self.texts = queries, texts
        self.processed_queries, self.processed_texts = [], []
        self.preprocess()

    def preprocess(self):
        self.processed_queries = [self.lemmatize(self.remove_stopwords(self.tokenize(q))) for q in self.queries]
        self.processed_texts = [self.lemmatize(self.remove_stopwords(self.tokenize(t))) for t in self.texts]
        return (self.processed_queries, self.processed_texts)

    def tokenize(self, sentence):
        return RegexpTokenizer(r'\w+').tokenize(sentence.lower())

    def remove_stopwords(self, tokens):
        return [w for w in tokens if not w in set(stopwords.words('english'))]

    def lemmatize(self, tokens):
        return [WordNetLemmatizer().lemmatize(w) for w in tokens]

    def main(self):
        for i in range(len(self.processed_queries)):
            self.find_best_texts(i)


    def show_output(self, data):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("QUERY:\n {}".format(data[1]))
        print("TEXT:\n {}".format(data[2]))
        print("SIMILITUDE PERCENTAGE: {} %".format(data[0]))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    def find_best_texts(self, iq):
        d,c,o,j,bag1 = [],[],[],[], BagOfWords(self.processed_queries[iq])
        for jt in range(len(self.processed_texts)):
            bag2 = BagOfWords(self.processed_texts[jt])
            d.append( (coef_dice(bag1, bag2), self.queries[iq], self.texts[jt]) )
            c.append( (coef_cosine(bag1, bag2), self.queries[iq], self.texts[jt]) )
            o.append( (coef_overlapping(bag1, bag2), self.queries[iq], self.texts[jt]) )
            j.append( (coef_jaccard(bag1, bag2), self.queries[iq], self.texts[jt]) )


        try:
            self.show_output(max(d)); self.show_output(max(c)); self.show_output(max(o)); self.show_output(max(j))
        except:
            pass

class BagOfWords(object):

    def __init__(self, values=None, text=None):
        self.values, self.text = values, text

        if self.values is None:
            self.values = {}

        if type(self.values) is not dict:
            self.values = string_to_bag_of_words(self.values)

        if self.text is not None:
            self.values = string_to_bag_of_words(self.text)

    def __str__(self):
        return str(dict(self.values))

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(zip(iter(self.values.keys()), iter(self.values.values())))

    def intersection(self, other):
        return BagOfWords(dict(self.values & other.values))

    def union(self, other):
        return BagOfWords(dict(self.values + other.values))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--queries_bank",
                        help="the PATH of a text file which contains a list of querys separated by a line break. Will be compared with each text",
                        nargs='?', const="cran-queries.txt", default="cran-queries.txt")

    parser.add_argument("--texts_bank",
                        help="the PATH of a text file which contains a list of texts separated by a line break. Will be compared by queries",
                        nargs='?', const="cran-1400.txt", default="cran-1400.txt")


    args = parser.parse_args()
    texts = [x.decode("utf-8") for x in file(args.texts_bank).readlines()]
    queries = [x.decode("utf-8") for x in file(args.queries_bank).readlines()]
    SimilarityChecker(queries, texts).main()
