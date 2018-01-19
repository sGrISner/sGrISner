#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

""" - FICHIER DE DEFINITION DES METHODES DE SELECTION DES ENTITES - """

import numpy as np
import random

class Strategy:
    def __init__(self):
        pass
    def filtre(buildings):
        pass

class Naive(Strategy):
    """Définition d'une fonction de sélection de toutes les entités présentes"""
    def filtre(buildings):
        return buildings

class Random(Strategy):
    """Définition d'une fonction de sélection d'entités aléatoiremenet sélectionnées"""
    def __init__(self, selection_number):
        self.selection_number = selection_number

    def filtre(buildings):
        return random.sample(buildings, self.selection_number)
