#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from collections import deque
from urlparse import urljoin
import requests, argparse, robotparser, time


"""
Author: Esteban Montes, UO246305
Description: A simple web crawler
"""

class Node(object):
    def __init__(self, url):
        self.url = url
        self.visited = False
        self.depth_level = 0
        self.adjacencies_list = []

    def add_neighbour(self, node):
        self.adjacencies_list.append(node)

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.url == other.url
        return False

    def __ne__(self, other):
        return not self.__eq__(other)



class SearchAlgorithms:
    """
    Simple class that are used for choose between differents
    exploration methods, taking a starter node and a limit
    """

    def __init__(self, origin_node, max_downloads):
        self.origin_node = origin_node
        self.max_downloads = max_downloads


    def execute_method(self, method):
        """
        Method that allows the exploration method execution,
        passing a string as parameter
        """

        self.method_type = {
            "bfs":self.bfs(),
            "dfs":self.dfs()
        }

        return self.method_type[method]


    def bfs(self):
        """
        Breadth First Search
        """
        queue, visited = deque(), set()
        queue.append(self.origin_node)
        visited.add(self.origin_node)

        while queue:
            current_node = queue.popleft()

            for node in current_node.adjacencies_list:
                if self.max_downloads == len(visited):
                    return [x.url for x in visited if x.url != self.origin_node.url]
                queue.append(node)
                visited.add(node)

        return [x.url for x in visited if x.url != self.origin_node.url]

    def dfs(self):
        """
        Depth First Search
        """
        stack, visited = [], set()
        stack.append(self.origin_node)

        while stack and self.max_downloads != len(visited):
            current_node = stack.pop()
            visited.add(current_node)
            map(lambda node: stack.append(node), current_node.adjacencies_list)

        return [x.url for x in visited if x.url != self.origin_node.url]



class WebCrawler:

    def __init__(self, url, max_downloads, waittime, robots, searchMethod):
        self.url = url
        self.max_downloads = max_downloads
        self.robots = robots
        self.origin_node = Node(url)
        self.waittime = waittime
        self.searchMethod = searchMethod

        self.rp = robotparser.RobotFileParser()
        self.robots_url = self.rp.set_url(url + "/robots.txt")


    def get_all_urls(self):
        return [x.get('href') for x in BeautifulSoup(self._get_request(self.url), "html.parser").find_all('a', href=True)]

    def _get_request(self, url):
        """
        Wrapper method for doing differents things for each GET request
        """
        if self.robots:
            self.rp.read()
            if self.rp.can_fetch("*", url):
                time.sleep(self.waittime)
                return requests.get(url, headers={"Content-type":"text/html"}).text


    def _normalize_url(self, url, link, predicates=None):
        """
        Method that filter each url as you want, you can add more
        predicates for filtering more situations just passing a dict as
        param, for example: take only domain or subdomain elements
        """
        default_predicates = {
            (link.startswith("javascript:")):"",
            (link.startswith("/") or link.startswith("#")):urljoin(url, link),
            (link.startswith("//")):link.replace("//", "")
        }

        if predicates is not None and type(predicates) is dict:
            default_predicates.update(predicates)

        for key, value in default_predicates.iteritems():
            if key:
                link = value

        return link


    def prepare_urls(self, urls):
        """
        Final method that normalize each url and get each one ready
        """
        return [x.replace("\n", "") for x in [self._normalize_url(self.url, x) for x in urls] if x is not None and x is not ""]


    def crawl(self):
        map(lambda url: self.origin_node.add_neighbour(Node(url)), self.prepare_urls(self.get_all_urls()))
        return SearchAlgorithms(self.origin_node, self.max_downloads).execute_method(self.searchMethod)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple script for crawling url's")

    parser.add_argument("url_bank", help = "The PATH of a text file which contains a list of url's separated by line break")
    parser.add_argument("max_downloads", help = "Limit of url's you will visit for each url", type=int)
    parser.add_argument("--waittime", help = "Time you must wait between requests AT SECONDS", type=int, nargs='?', const=0, default=0)
    parser.add_argument("--robots", help = "Do you want to follow robots.txt for crawling <<legally>>? TRUE/FALSE", type=bool,nargs='?',const=True, default=True)
    parser.add_argument("--searchMethod", help = "Indicate which kind of search method you want", nargs='?', const="bfs", default="bfs")

    args = parser.parse_args()

    for url in [x.replace("\n", "") for x in file(args.url_bank).readlines()]:
        print("Crawling: %s using: %s as exploration method" % (url, args.searchMethod))
        print("---------------------------------------------")

        try:
            print("\n".join(WebCrawler(url, args.max_downloads, args.waittime, args.robots, args.searchMethod).crawl()))
        except:
            print("Couldn't fetch data from: %s" % url)

        print("---------------------------------------------\n")
