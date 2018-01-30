#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

""" - FICHIER DE DEFINITION DES METHODES DE SELECTION DES ENTITES - """

import numpy as np
import random


class Strategy:
    def __init__(self):
        pass

    def filtre(self, buildings):
        pass


class Naive(Strategy):
    """
    Naive selection strategy
    """
    def __init__(self):
        super().__init__()

    def filtre(self, buildings):
        return buildings


class Random(Strategy):
    """
    Random selection strategy
    """
    def __init__(self, selection_number):
        super().__init__()
        self.selection_number = selection_number

    def filtre(self, buildings):
        return random.sample(buildings, self.selection_number)
