# -*- encoding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division


class Graph(object):
    def __init__(self, edges):
        self.edges = edges
        self.inlink_map, self.outlink_counts, self.ranking = {},{},{}

    def _get_all_nodes(self):
        return set(self.inlink_map.keys())

    def _create_node(self, node):
        if node not in self.inlink_map: self.inlink_map[node] = set()
        if node not in self.outlink_counts: self.outlink_counts[node] = 0

    def _load_graph_data(self):
        for origin, dest in self.edges:
            self._create_node(origin), self._create_node(dest)
            #if origin == dest:  continue
            if origin not in self.inlink_map[dest]:
                self.inlink_map[dest].add(origin); self.outlink_counts[origin] += 1

    def _set_initial_values(self):
        for node in self.inlink_map.keys(): self.ranking[node] = 1/len(self._get_all_nodes())

    def page_rank(self, damping=0.85, limit=1.0e-8):
        self._load_graph_data(); self._set_initial_values()
        norm = 1.0
        while norm > limit:
            ranking = {}
            for node, inlinks in self.inlink_map.items():
                ranking[node] = ((1 - damping) / len(self._get_all_nodes())) + (damping * sum(self.ranking[inlink] / self.outlink_counts[inlink] for inlink in inlinks))
            norm, self.ranking, ranking = sum(abs(ranking[node] - self.ranking[node]) for node in ranking.keys()), ranking, self.ranking

        return self.ranking

"""
if "__main__":
    edges = [
        ["A", "B"],
        ["A", "C"],
        ["A", "F"],
        ["B", "A"],
        ["B", "C"],
        ["B", "D"],
        ["C", "F"],
        ["D", "A"],
        ["D", "C"],
        ["D", "E"],
        #["E", "E"],
        #["E", "A"],
        #["E", "C"],
        ["F", "C"],
        ["F", "D"],
        ["F", "E"],
    ]
"""
"""
g = Graph(edges)
print(g.page_rank())
"""
