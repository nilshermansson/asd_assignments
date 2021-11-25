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
    """
        Sig:  weightlifting(P, weight), Set[int], int -> bool
        Pre:  weight > 0, all plates in P are > 0 
        Post:
        Ex:
            weightlifting({7, 8, 9}, 15 = True)
            weightlifting({7, 8, 9}, 18 = False)
    """

    plate_list = sorted(P)
    if len(P) == 0:
        return weight == 0

    dp_matrix = [[False for i in range(weight + 1)]
                                       for j in range(len(plate_list) + 1)]

    for i in range(len(plate_list) + 1):
        #Variant: len(plate_list) + 1 - i
        for j in range(weight + 1):
            #Variant: weight + 1 - j
            if j == 0:
                dp_matrix[i][j] = True
            elif i == 0:
                dp_matrix[i][j] = False
            else:
                if plate_list[i - 1] > j:
                    dp_matrix[i][j] = dp_matrix[i - 1][j]
                else:
                    dp_matrix[i][j] = dp_matrix[i -1][j] or dp_matrix[i - 1][j - plate_list[i - 1]]
    return dp_matrix[-1][-1]


def weightlifting_subset(P: Set[int], weight: int) -> Set[int]:
    """
        Sig:  weightlifting_subset(P, weight), Set[int], int -> Set[int]
        Pre:  weight > 0, all plates in P are > 0 
        Post:
        Ex:
            weightlifting({7, 8, 9}, 15 = {7, 8})
            weightlifting({7, 8, 9}, 18 = {})
    """


    plate_list = list(P)

    dp_matrix = [[False for i in range(weight + 1)]
                                       for j in range(len(plate_list) + 1)]

    res = set()
    for i in range(len(plate_list) + 1):
        #Variant: len(plate_list) + 1 - i
        for j in range(weight + 1):
            #Variant: weight + 1 - j
            if j == 0:
                dp_matrix[i][j] = True
            elif i == 0:
                dp_matrix[i][j] = False
            else:
                if plate_list[i - 1] > j:
                    dp_matrix[i][j] = dp_matrix[i - 1][j]
                else:
                    v1 = dp_matrix[i - 1][j]
                    v2 = dp_matrix[i - 1][j - plate_list[i - 1]]
                    dp_matrix[i][j] = v1 or v2
    
    if dp_matrix[-1][-1] == True:
        i = len(plate_list)
        while weight != 0:
            #Variant: weight
            current_plate = plate_list[i-1]
            if current_plate <= weight and dp_matrix[i - 1][weight - current_plate]:
                res.add(current_plate)
                weight -= current_plate
            i = i - 1
    return res


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

    plates = {2, 32, 234, 35, 12332, 1, 7, 56}
    plates = {75, 85, 86}
    print(weightlifting_subset(plates, 160))