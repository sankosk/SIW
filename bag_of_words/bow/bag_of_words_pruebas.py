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
    """
    Method that tokenize a sentence, remove puntuaction symbols and stopwords,
    take their lexemes and return a Counter object (dict child)
    """
    lemmatizer, tokens = WordNetLemmatizer(), RegexpTokenizer(r'\w+').tokenize(text.lower())
    tokens = [w for w in tokens if not w in set(stopwords.words('english'))]
    return Counter([lemmatizer.lemmatize(w) for w in tokens])


def main(args):
    """
    Main method, loads the files to compare and checks for the best text similitude
    with each query
    """
    texts = file(args.texts_bank).readlines()[:args.text_limit]
    queries = file(args.queries_bank).readlines()[:args.query_limit]
    for q in queries:   find_best_texts(q, texts, args.show_text)


def show_output(data, flag):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("QUERY:\n {}".format(data[0]))
    print("TEXT:\n {}".format(data[1]) if flag else "")
    print("COEF METHOD: {}".format(data[3].upper()))
    print("SIMILITUDE PERCENTAGE: {} %".format(float(data[2]) * 100))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


"""
def find_best_text(q, texts, coef_method, coef_method_name):
    return max([(q.strip(), l.strip(), coef_method(BagOfWords(q.strip()), BagOfWords(l.strip())), coef_method_name) for l in texts])
"""

def find_best_texts(q, texts, flag):
    """
    Method that set a score for each text using different methods
    and show us the best scored text.
    PD: Is not the best way to showing up the results,
    but is faster in this case (predefined methods for calculating the score)
    """
    d,c,i,j = [],[],[],[]
    for text in texts:
        d.append( (q.strip(), text.strip(), coef_dice(BagOfWords(q.strip()), BagOfWords(text.strip())), "dice") )
        c.append( (q.strip(), text.strip(), coef_cosine(BagOfWords(q.strip()), BagOfWords(text.strip())), "cosine") )
        i.append( (q.strip(), text.strip(), coef_overlapping(BagOfWords(q.strip()), BagOfWords(text.strip())), "overlapping") )
        j.append( (q.strip(), text.strip(), coef_jaccard(BagOfWords(q.strip()), BagOfWords(text.strip())), "jaccard") )

    show_output( max(d),flag ); show_output( max(c),flag ); show_output( max(i),flag ); show_output( max(j),flag )




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

    parser.add_argument("--query_limit",
                        help="Limit of how much queries you want to compare",
                        type=int, nargs='?', const=10, default=10)

    parser.add_argument("--text_limit",
                        help="Limit of how much texts will be compared by these queries",
                        type=int, nargs='?', const=10, default=10)

    parser.add_argument("--show_text",
                        help="Text which is being compared with the query",
                        type=bool, nargs='?', const=False, default=False)

    exit(main(parser.parse_args()))


    #texts = [l.strip() for l in file("cran-1400.txt").readlines()[:args.text_limit]]
    #queries = [l[5::].strip() for l in file("cran-queries.txt").readlines()[:args.query_limit]]
