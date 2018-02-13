#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" FICHIER DE DEFINITION DES METHODES DE SELECTION DES ENTITES """

import numpy as np
import random

import inspect


class Strategy:
    """
    CLASSE STRATEGIE

    METHODES:
    ==========
        - filtre(buildings=liste): filtrage d'une liste données.
    """

    def __init__(self):
        pass

    def filtre(self, buildings):
        pass


class Naive(Strategy):
    """
    STRATEGIE NAIVE

    HERITAGE : Classe Strategy
    ==========

    METHODES:
    ==========
        - filtre(buildings=liste): retourne la liste d'entrée.
    """

    def __init__(self):
        super().__init__()

    def filtre(self, buildings):
        return buildings


class Random(Strategy):
    """
    STRATEGIE RANDOM

    HERITAGE : Classe Strategy
    ==========

    ATTRIBUTS :
    ==========
        - selection_number: nombre d'entités à sélectionner.

    METHODES :
    ==========
        - filtre(buildings=filtre):
            retourne un nombre donné d'objet de la liste, aléatoirement sélectionnés.
    """
    def __init__(self, selection_number):
        super().__init__()
        self.selection_number = selection_number

    def filtre(self, buildings):
        return random.sample(buildings, self.selection_number)


STRATEGIES = {
    strategy.__name__: (
        inspect.getargspec(strategy.__init__),
        inspect.getargspec(strategy.filtre)
    )
    for strategy in Strategy.__subclasses__()
}
