#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 1, Problem 1: Weightlifting

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
from src.weightlifting_data import data  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['weightlifting', 'weightlifting_subset']

def weightlifting(P: Set[int], weight: int) -> bool:
    plate_list = list(P)
    dp_matrix = [[False for i in range(weight + 1)] for j in range(len(plate_list) + 1)]

    for i in range(len(plate_list) + 1):
        for j in range(weight+ 1):
            if j == 0:
                dp_matrix[i][j] = True
            else: 
                if plate_list[i - 1] > j:
                    dp_matrix[i][j] = dp_matrix[i - 1][j]
                else:
                    dp_matrix[i][j] = dp_matrix[i - 1][j] or dp_matrix[i - 1][j - plate_list[i - 1]]
    return dp_matrix[-1][-1]

def weightlifting_subset(P: Set[int], weight: int) -> Set[int]:
  '''
    Sig:  Set[int], int -> Set[int]
    Pre:
    Post:
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting_subset(P, 299) = {56, 7, 234, 2}
          weightlifting_subset(P, 11) = {}
  '''
  plate_list = list(P)
  dp_matrix = [[None for i in range(weight + 1)] for j in range(len(plate_list) + 1)]
  


'''
def weightlifting(P: Set[int], weight: int) -> bool:
    plate_list = list(P)
    dp_matrix = [[None for i in range(weight + 1)] for j in range(len(plate_list) + 1)]
    def weightlifting_aux(P: Set[int], weight: int) -> bool:
        # base cases
        if weight == 0:
            return True
        elif len(P) == 0 or weight < 0:
            return False
        # do we have the result from this cached?
        elif dp_matrix[len(P)][weight] != None:
            return dp_matrix[len(P)][weight]
        # branch
        else:
            P2 = P.copy()
            current_plate = P2.pop()
            dp_matrix[len(P)][weight] = weightlifting_aux(P2, weight) or weightlifting_aux(P2, weight - current_plate)
            return dp_matrix[len(P)][weight]
    return weightlifting_aux(P, weight)


def weightlifting_subset(P: Set[int], weight: int) -> Set[int]:
    Sig:  Set[int], int -> Set[int]
    Pre:
    Post:
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting_subset(P, 299) = {56, 7, 234, 2}
          weightlifting_subset(P, 11) = {}
    plate_list = list(P)
    dp_matrix = [[None for i in range(weight + 1)] for j in range(len(plate_list) + 1)]
    res = set()

    def weightlifting_aux(P: Set[int], weight: int) -> bool:
        # base cases
        if weight == 0:
            dp_matrix[len(P)][weight] = True
            return True
        elif len(P) == 0 or weight < 0:
            return False
        # do we have the result from this cached?
        elif dp_matrix[len(P)][weight] != None:
            return dp_matrix[len(P)][weight]
        # branch
        else:
            P2 = P.copy()
            current_plate = P2.pop()
            dp_matrix[len(P)][weight] = weightlifting_aux(P2, weight) or weightlifting_aux(P2, weight - current_plate)
            if dp_matrix[len(P)][weight]:
                res.add(current_plate)
            return dp_matrix[len(P)][weight]

    
    # Unclear
    print(f'Running subset for P = {P} and weight = {weight}')
    if (weightlifting_aux(P, weight)):
        while weight:
            current_plate = P.pop()
            if current_plate <= weight and dp_matrix[len(P)][weight - current_plate] == True:
                res.add(current_plate)
                weight = weight - current_plate

    return res 

'''

class WeightliftingTest(unittest.TestCase):
    """
    Test Suite for weightlifting problem

    Any method named "test_something" will be run when this file is executed.
    Use the sanity check as a template for adding your own test cases if you
    wish. (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('WeightLiftingTest')
    data = data
    weightlifting = weightlifting
    weightlifting_subset = weightlifting_subset

    def test_satisfy_sanity(self):
        """
        Sanity Test for weightlifting()

        passing is not a guarantee of correctness.
        """
        plates = {2, 32, 234, 35, 12332, 1, 7, 56}
        self.assertTrue(
            WeightliftingTest.weightlifting(plates, 299)
        )
        self.assertFalse(
            WeightliftingTest.weightlifting(plates, 11)
        )
    def test_subset_sanity(self):
        """
        Sanity Test for weightlifting_subset()

        passing is not a guarantee of correctness.
        """
        plates = {2, 32, 234, 35, 12332, 1, 7, 56}
        weight = 299
        sub = WeightliftingTest.weightlifting_subset(plates, weight)
        for p in sub:
            self.assertIn(p, plates)
        self.assertEqual(sum(sub), weight)

        weight = 11
        sub = WeightliftingTest.weightlifting_subset(plates, weight)
        self.assertSetEqual(sub, set())

    def test_satisfy(self):
        for instance in self.data:
            self.assertEqual(
                WeightliftingTest.weightlifting(instance["plates"],
                                                instance["weight"]),
                instance["expected"]
            )

    def test_subset(self):
        """
        Sanity Test for weightlifting_subset()

        passing is not a guarantee of correctness.
        """
        for instance in self.data:
            plates = WeightliftingTest.weightlifting_subset(
                instance["plates"].copy(),
                instance["weight"]
            )
            self.assertEqual(type(plates), set)

            for plate in plates:
                self.assertIn(plate, instance["plates"])

            if instance["expected"]:
                self.assertEqual(
                    sum(plates),
                    instance["weight"]
                )
            else:
                self.assertSetEqual(
                    plates,
                    set()
                )


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

    '''
    plates = {2, 32, 234, 35, 12332, 1, 7, 56}
    plates = {2, 4, 5, 8, 9, 10, 33, 45}
    plates = {100, 2, -1}
    print(weightlifting_it(plates, 101))
    '''