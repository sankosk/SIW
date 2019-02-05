#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import argparse, string, nltk, io, json, math
from pprint import pprint
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

"""
Author: Esteban Montes Morales, UO246305
"""

class Indexer(object):

    def __init__(self):
        self.docs_index, self.words_index, self.doc_length = [], {}, 0
        self._tf, self._idf = lambda c,s: c/s, lambda w: math.log10(self.doc_length/len(self.words_index[w]))

    def index(self, bag):
        bdata = lambda v: [[bag.values[v],bag.document_len()],self.doc_length]
        for value in bag.values:
            if value in self.words_index:
                self.words_index[value].append(bdata(value))
            else:
                self.words_index[value] = [bdata(value)]
        self.docs_index.append(bag.values); self.doc_length += 1

    def score(self, w, enable_stemming=False, filter_stopwords=False):
        wfr, sw, n =lambda d: d[0][0], lambda d: d[0][1], lambda d: d[1]
        return [[self._tf(wfr(d), sw(d)) * self._idf(w), n(d)] for d in self.words_index[w]]

    def dump(self, io):
        json.dump({"docs_index":self.docs_index, "words_index":self.words_index}, io)



class BagOfWords(object):
    def __init__(self, values=None, text=None, enable_stemming=False, filter_stopwords=False):
        self.values, self.text = values, text
        self.enable_stemming, self.filter_stopwords = enable_stemming, filter_stopwords

        if self.values is None:
            self.values = {}

        if type(self.values) is not dict:
            self.values = self.string_to_bag_of_words(self.values)

        if self.text is not None:
            self.values = self.string_to_bag_of_words(self.text)

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

    def document_len(self):
        return reduce(lambda a,b: a+b, self.values.itervalues())

    def string_to_bag_of_words(self, text):
        text = RegexpTokenizer(r'\w+').tokenize(text.lower())

        if not(self.enable_stemming) and not(self.filter_stopwords):
            return Counter(text)

        elif not(self.enable_stemming) and self.filter_stopwords:
            stop_words = set(nltk.corpus.stopwords.words('english'))
            return Counter([x for x in text if not x in stop_words])

        elif self.enable_stemming and not(self.filter_stopwords):
            return Counter([WordNetLemmatizer().lemmatize(x) for x in text])

        else:
            stop_words = set(nltk.corpus.stopwords.words('english'))
            return Counter([WordNetLemmatizer().lemmatize(x) for x in text if not x in stop_words])


def main(args):
    indexer = Indexer()
    [indexer.index(BagOfWords(f)) for f in file(args.inputFile).readlines()]
    with open(args.outputFile, 'w+') as output:
        indexer.dump(output)


def parse_args():
    parser = argparse.ArgumentParser(description="tf-idf table implementation")
    parser.add_argument("--inputFile", help="corpus file path to index", nargs='?', const="cran-1400.txt", default="cran-1400.txt")
    parser.add_argument("--outputFile", help="filename of the index generated as .json", nargs='?', const="indexed-cran-1400.json", default="indexed-cran-1400.json")
    return parser.parse_args()

if __name__ == '__main__':
    exit(main(parse_args()))
