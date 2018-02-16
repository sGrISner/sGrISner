#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
    ``Strategies`` module.
    ======================

    Defines an interface like structure for strategies:

    1. Naive strategy
    -------------------

    Defines the naive strategy where you need all samples. It is suitable for
    annotation correction.

    2. Random strategy
    -------------------

    Defines the random strategy where you sample randomly among input samples.
    It is suitable for annotation verification.
"""

__docformat__ = 'reStructuredText'


import numpy as np
import random


class Strategy:
    """
        Strategy interface.
    """

    def __init__(self):
        """
            Initiate `Strategy`.
        """
        pass

    def filter(self, buildings):
        """
            Virtual method to filter input.

            :param buildings: Buildings list to filter
            :type buildings: list
        """
        pass


class Naive(Strategy):
    """
        Naive strategy.

        Extends `Strategy`.
    """

    def __init__(self):
        """
            Extend `Strategy` to initiate `Naive`.
        """
        super().__init__()

    def filter(self, buildings):
        """
            Filter inputs.

            :param buildings: Buildings list to filter
            :type buildings: list
            :return: filtered buildings to show. i.e. all of them
            :rtype: list
        """
        return buildings


class Random(Strategy):
    """
        Random strategy.

        Extends `Strategy`. Attribute `selection_number` represents the number
        of samples to return.
    """

    def __init__(self, selection_number):
        """
            Extend `Strategy` to initiate `Random.selection_number`.
        """
        super().__init__()
        self.selection_number = selection_number

    def filter(self, buildings):
        """
            Filter `selection_number` inputs randomly.

            :param buildings: Buildings list to filter
            :type buildings: list
            :return: filtered buildings to show. i.e. all of them
            :rtype: list
        """
        return random.sample(buildings, self.selection_number)
