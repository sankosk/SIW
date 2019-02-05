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
        self._tf, self._idf = lambda c,s: c/s, lambda w: 1 + math.log(self.doc_length/len(self.words_index[w]))

    def index(self, bag):
        bdata = lambda v: [[bag.values[v],bag.document_len()],self.doc_length]
        for value in bag.values:
            if value in self.words_index:
                self.words_index[value].append(bdata(value))
            else:
                self.words_index[value] = [bdata(value)]
        self.docs_index.append(bag); self.doc_length += 1

    def score(self, w, enable_stemming=False, filter_stopwords=False):
        wfr, sw, n =lambda d: d[0][0], lambda d: d[0][1], lambda d: d[1]
        return [[self._tf(wfr(d), sw(d)) * self._idf(w), n(d)] for d in self.words_index[w]]

    def dump(self, io):
        json.dump({"docs_index":[x.to_dict() for x in self.docs_index], "terms_index":self.words_index}, io)

    def load(self, fd):
        got = json.load(fd)
        self.docs_index, self.words_index = [BagOfWords.from_dict(x) for x in got["docs_index"]], got["terms_index"]
        self.doc_length += len(got["docs_index"])

    def to_dict(self):
        return {"docs_index":[x.to_dict() for x in self.docs_index], "terms_index":self.words_index}

    def _cosine_similarity(self,query, document):
        dot_product = sum([query[t]*document[t] for t in query if t in document])
        query_module = math.sqrt(sum([query[x]**2 for x in query]))
        doc_module = math.sqrt(sum([document[x]**2 for x in document]))
        return dot_product / (query_module * doc_module)

    def _get_search_results(self, queries_table, docs_table, n):
        result = [(self.docs_index[d].text, self._cosine_similarity(queries_table, docs_table[d])) for d in docs_table]
        return sorted(((text, round(score, 5)) for text, score in result), reverse=True, key=lambda x: (x[1], x[0]))[0:n]


    def search(self, query, n):
        queries_table, docs_table = {}, {}
        for term in query.values:
            tf_query_term = query.values[term] / query.document_len()
            if term in self.words_index:
                idf = 1 + math.log(self.doc_length / len(self.words_index[term]))
                candidate_docs = {d[1] for d in self.words_index[term]}
                cd_info = [i for i in self.words_index[term] if i[1] in candidate_docs]

                for document in cd_info:
                    tf = document[0][0] / document[0][1]
                    tf_idf = tf*idf
                    num_doc = document[1]
                    if num_doc not in docs_table:
                        docs_table[num_doc] = {}
                    docs_table[num_doc][term] = tf_idf
            else:
                idf = 1 + math.log(self.doc_length + 1)

            queries_table[term] = tf_query_term * idf

        return self._get_search_results(queries_table, docs_table, n)

class BagOfWords(object):
    def __init__(self, values=None, text=None, enable_stemming=False, filter_stopwords=False):
        self.values, self.text = values, text
        self.enable_stemming, self.filter_stopwords = enable_stemming, filter_stopwords

        if self.values is None:
            self.values = {}

        if type(self.values) is not dict:
            self.text = self.values
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

    def to_dict(self):
        return {"text":self.text, "values":dict(self.values)}

    @classmethod
    def from_dict(self,d):
        try:
            return BagOfWords(text=d["text"], values=d["values"])
        except:
            raise ValueError()

    @classmethod
    def from_values_dict(self,v):
        return BagOfWords(values=v)

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
