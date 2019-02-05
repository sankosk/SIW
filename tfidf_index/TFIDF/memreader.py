#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from indexer import Indexer
import argparse, json

def main(args):
    index = json.load(file(args.inputFile))
    try:
        docs = index["words_index"][args.searchWord]
        for doc in docs:
            print("Doc: %d, <<%s>> appears: %d times\n" % (doc[1], args.searchWord ,doc[0][0]))
    except:
        print("The word was not found at any document")


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--inputFile", help="json file with the data of the index", nargs='?', const="indexed-cran-1400.json", default="indexed-cran-1400.json")
    parser.add_argument("--searchWord", help="word to search", nargs='?', const="expanded", default="expanded")
    return parser.parse_args()

if __name__ == '__main__':
    exit(main(parse_args()))
