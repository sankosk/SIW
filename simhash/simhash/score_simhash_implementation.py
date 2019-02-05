# -*- encoding:utf-8 -*-

# Este fichero compara el valor obtenido con el valor experado y da un score al metodo implentado

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import io
import difflib
import argparse


def main(args):
    try:
        python_file = args.file
        if python_file.endswith(".py"):
            python_file = python_file[:-3]
        implementation = __import__(python_file)
        simhash = implementation.simhash
    except ImportError:
        print("Unable to import: {}".format(args.file))
        return 1
    except AttributeError:
        print("The Python file must define simhash: {}".format(args.file))
        return 1
    score_implementation(simhash, args.restrictiveness, args.ngram)
    return 0


def score_implementation(simhash, restrictiveness, ngram):
    expected_matches = read_truth("./articles_10000.truth")
    index = create_index("./articles_10000.train", simhash, restrictiveness, ngram)
    got_matches = get_matches(index)
    #print("\n" + ">" * 80)
    #print("- EXPECTED MATCHES")
    #print("+ GOT MATCHES")
    #print(">" * 80)
    #print_matches_comparation(expected_matches, got_matches)
    #print("<" * 80)
    print_score(expected_matches, got_matches)


def create_index(file, simhash, restrictiveness, ngram_len):
    index = {}
    with io.open(file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            args = [line, restrictiveness]
            if ngram_len:
                args.append(ngram_len)
            try:
                hash = simhash(*args)
            except TypeError:
                if ngram_len:
                    print("Has intentado llamar a una implmenentación de simhash que no soporta n-gramas con el parametro ngram={}".format(ngram_len))
                else:
                    print("Has intentado llamar a una implmenentación de simhash que utiliza n-gramas con el parametro ngram={}".format(ngram_len))
                exit(1)
            try:
                index[hash].append(line)
            except:
                index[hash] = [line]
    return index


def get_matches(index):
    return tuple(sorted([" == ".join(sorted(line.split(" ")[0] for line in lines)) for _, lines in index.iteritems() if len(lines) > 1]))

def print_matches_comparation(expected_matches, got_matches):
    for line in difflib.ndiff(expected_matches, got_matches):
        print(line)


def print_score(expected_matches, got_matches):
    s1 = set(expected_matches)
    s2 = set(got_matches)
    score = len(s1.intersection(s2)) / len(s1.union(s2))
    print("SCORE: {}".format(score))


def read_truth(text):
    matches = []
    with io.open(text, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            matches.append(" == ".join(sorted(line.split(" "))))
    return tuple(sorted(matches))


def parse_args():
    parser = argparse.ArgumentParser(description='Test and score SimHash implmentations')
    parser.add_argument("file", help="Python file")
    parser.add_argument("-r", "--restrictiveness", type=int, default=10, help="Use %(default)s hashes")
    parser.add_argument("-n", "--ngram", type=int, default=0, help="Use N-grams with length %(default)s. 0 means no ngrams")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    exit(main(parse_args()))
