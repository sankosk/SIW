# -*- encoding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from pagerank import Graph
import argparse

def main(args):
    file_content = file("graph-example.txt").readlines()
    edges = [line.strip().split(",") for line in file_content]
    print(Graph(edges).page_rank())

def parse_args():
    parser = argparse.ArgumentParser(description="Pagerank implementation")
    parser.add_argument("-fg",
                        "--filegraph",
                        nargs='?', const="graph-example.txt", default="graph-example.txt",
                        help="Path of the file that contains the graph")

    return parser.parse_args()

exit(main(parse_args()))
