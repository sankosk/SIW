#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import argparse, gzip, json
from SimHash import simhash, parse_args

def main(args):
    index = {}
    with gzip.open(args.texts) as f:
        for line in f:
            line = line.decode("utf-8")
            line = line.strip()
            data = json.loads(line)
            if data["_source"]["lang"] != "en":
                continue
            line = data["_source"]["text"]
            hash = simhash(line, args.restrictiveness)
            if hash is None:
                continue
            try:
                index[hash].append(line)
            except:
                index[hash] = [line]
        for _, lines in index.iteritems():
            if len(lines) > 1:
                print("\n\n\n")
            print("FOUND:")
            for line in lines:
                print(">" * 80)
                print(line[0:args.show].encode("utf-8"))
                print("<" * 80)

if __name__ == '__main__':
    exit(main(parse_args()))

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