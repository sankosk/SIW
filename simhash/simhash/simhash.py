#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Esteban Montes, UO246305
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse, string, nltk, binascii, io
from pprint import pprint
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


def main(args):
    prev = dict()
    with open(args.texts) as f:
        for line in f:
            line = line.decode("utf-8")
            line = line.strip()
            h = simhash(line,args.restrictiveness)
            if h is None:
                continue
            if h in prev:
                prev[h].append(line)
            else:
                prev[h] = [line]
    for element in prev:
        if len(prev[element]) > 1:
            print("\n\n HASH: " + str(element) + "\n\n")
            for sub in prev[element]:
                print(sub)
                print("\n")
            print("\n")


def simhash(line, restrictiveness):
    v = BagOfWords(line)
    return calculate_hashes(v,restrictiveness) if len(v)!=0 else None


def calculate_hashes(vector, restrictiveness):
    hashes = [ binascii.crc32(w[0].encode("utf-8")) & 0xffffffff for w in vector]; hashes.sort()
    return reduce(lambda a,b: a^b, hashes[:restrictiveness])


class BagOfWords(object):
    def __init__(self, values=None, text=None):
        self.values, self.text = values, text

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

    def string_to_bag_of_words(self, text):
        text = RegexpTokenizer(r'\w+').tokenize(text.lower())
        stop_words = set(nltk.corpus.stopwords.words('english'))
        return Counter([WordNetLemmatizer().lemmatize(x) for x in text if not x in stop_words])


def parse_args():
    parser = argparse.ArgumentParser(description='SimHash')
    parser.add_argument("texts", help="Texts file")
    parser.add_argument(
        "-r",
        "--restrictiveness",
        type=int,
        default=6,
        help="Use %(default)s hashes")
    parser.add_argument(
        "-s",
        "--show",
        type=int,
        default=-1,
        help="Show only %(default)s lines in each found line. -1 means all")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())


