#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 1: Controlling the Maximum Flow

Team Number:
Student Names:
'''

'''
Copyright: justin.pearson@it.uu.se and his teaching assistants, 2020.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
'''
from typing import *  # noqa
import unittest  # noqa
import math  # noqa
from src.sensitive_data import data  # noqa
from src.graph import Graph  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['sensitive']


def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    visited = set()

    def dfs(G: Graph, s: str, t: str):
        visited.add(s)
        if s == t:
            return True

        for neighbor in G.neighbors(s):
            if neighbor not in visited:
                if G.flow(s, neighbor) < G.capacity(s, neighbor):
                    if dfs(G, neighbor, t):
                        return True
        return False
    residual_G = Graph(is_directed = True)
    for edge in G.edges:
        # add_edge(u, v, weight, capacity, flow)
        # remove_edge(u, v)
        res_u, res_v = edge
        residual_G.add_edge(res_v, res_u, capacity = G.capacity(res_u, res_v), flow = G.flow(res_u, res_v))

    all_edges = residual_G.edges
    capped_edges = []

    # Get all capped edges
    for edge in all_edges:
        u, v = edge
        if residual_G.flow(u, v) == residual_G.capacity(u, v) and residual_G.flow(u, v) > 0:
            capped_edges.append(edge)
    
    res = []
    for edge in capped_edges:
        # Increment capacity of edge
        u, v = edge
        og_capacity = residual_G.capacity(u, v)
        residual_G.set_capacity(u, v, og_capacity + 1)

        visited = set()
        found_path =  dfs(residual_G, t, s)
        residual_G.set_capacity(u, v, og_capacity)

        # Reset capacity

        if found_path:
            return (v, u)
    return None, None


class SensitiveTest(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    logger = logging.getLogger('SensitiveTest')
    data = data
    sensitive = sensitive

    def test_sanity(self):
        """Sanity check"""
        g1 = Graph(is_directed=True)
        g1.add_edge('a', 'b', capacity=16, flow=12)
        g1.add_edge('a', 'c', capacity=13, flow=11)
        g1.add_edge('b', 'd', capacity=12, flow=12)
        g1.add_edge('c', 'b', capacity=4, flow=0)
        g1.add_edge('c', 'e', capacity=14, flow=11)
        g1.add_edge('d', 'c', capacity=9, flow=0)
        g1.add_edge('d', 'f', capacity=20, flow=19)
        g1.add_edge('e', 'd', capacity=7, flow=7)
        g1.add_edge('e', 'f', capacity=4, flow=4)
        self.assertIn(
            SensitiveTest.sensitive(g1, 'a', 'f'),
            {('b', 'd'), ('e', 'd'), ('e', 'f')}
        )
        g2 = Graph(is_directed=True)
        g2.add_edge('a', 'b', capacity=1, flow=1)
        g2.add_edge('a', 'c', capacity=100, flow=4)
        g2.add_edge('b', 'c', capacity=100, flow=1)
        g2.add_edge('c', 'd', capacity=5, flow=5)
        self.assertEqual(
            SensitiveTest.sensitive(g2, 'a', 'd'),
            ('c', 'd')
        )
        g3 = Graph(is_directed=True)
        g3.add_edge('a', 'b', capacity=1, flow=1)
        self.assertEqual(
            SensitiveTest.sensitive(g3, 'a', 'b'),
            ('a', 'b')
        )
        g4 = Graph(is_directed=True)
        g4.add_edge('a', 'b', capacity=0, flow=0)
        self.assertEqual(
            SensitiveTest.sensitive(g4, 'a', 'b'),
            (None, None)
        )
        g5 = Graph(is_directed=True)
        for u, v in g1.edges:
            g5.add_edge(u, v, capacity=0, flow=0)
        self.assertEqual(
            SensitiveTest.sensitive(g5, 'a', 'f'),
            (None, None)
        )
        

    def test_sensitive(self):
        for instance in SensitiveTest.data:
            graph = instance['digraph'].copy()
            u, v = SensitiveTest.sensitive(
                graph,
                instance["source"],
                instance["sink"]
            )
            self.assertIn(u, graph, f"Invalid edge ({u}, {v})")
            self.assertIn((u, v), graph, f"Invalid edge ({u}, {v})")
            self.assertIn(
                (u, v),
                instance["sensitive_edges"]
            )


if __name__ == "__main__":
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
