#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 2: Party Seating

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
from src.party_seating_data import data  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['party']


def party(known: List[Set[int]]) -> Tuple[bool, Set[int], Set[int]]:
    """
    Sig:  List[Set[int]] -> Tuple[bool, Set[int], Set[int]]
    Ex:   party([{1, 2}, {0}, {0}]) = True, {0}, {1, 2}
    """
    tables = [set(), set()]
    def search(me: int, my_table: int):
        # Variant: number of guests not in tables[0] or tables[1]
        """
        Sig:  int, int -> void
        Pre:  tables exists and is a list of two empty sets
        Post: tables[0] and tables[1] is populated with integers 
              representing each pearson to be seated at each respective 
              table
        """
        if me in tables[my_table]:
            return True
        
        tables[my_table].add(me)
        for neighbor in known[me]:
            # Variant: number of neighbors not in tables[0] or tables[1]
            if neighbor in tables[my_table]:
                return False
            else:
                if not search(neighbor, (my_table + 1) % 2):
                    return False
        return True

    for i in range(len(known)):
        # Variant: len(known)
        if not (i in tables[0] or i in tables[1]):
            if not search(i, 0):
                return False, set(), set()
    return True, tables[0], tables[1]

class PartySeatingTest(unittest.TestCase):
    """
    Test suite for party seating problem
    """
    logger = logging.getLogger('PartySeatingTest')
    data = data
    party = party

    def known_test(self, known, A, B):
        self.assertEqual(
            len(A) + len(B),
            len(known),
            "wrong number of guests: "
            f"{len(known)} guests, "
            f"tables hold {len(A)} and {len(B)}"
        )
        for g in range(len(known)):
            self.assertTrue(
                g in A or g in B,
                f"Guest {g} not seated anywhere"
            )
        for a1, a2 in ((a1, a2) for a2 in A for a1 in A):
            self.assertNotIn(
                a2,
                known[a1],
                f"Guests {a1} and {a2} seated together, and know each other"
            )
        for b1, b2 in ((b1, b2) for b2 in B for b1 in B):
            self.assertNotIn(
                b2,
                known[b1],
                f"Guests {b1} and {b2} seated together, and know each other"
            )

    def test_sanity(self):
        """
        Sanity test

        A minimal test case.
        """
        known = [{1, 2}, {0}, {0}]
        _, A, B = PartySeatingTest.party(known)
        self.known_test(known, A, B)

    def test_party(self):
        for instance in PartySeatingTest.data:
            known = instance["known"]
            expected = instance["expected"]
            success, A, B = PartySeatingTest.party(known)

            if not expected:
                self.assertFalse(success)
                continue
            self.known_test(known, A, B)


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
