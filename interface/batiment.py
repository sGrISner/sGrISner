#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

""" - FICHIER DE DEFINITION DE LA CLASSE BATIMENT - """

class Batiment:
    """--- OBJET BATIMENT ---

    ATTRIBUTS :
    ===========
        - identity = identifiant de l'entité
        - geometry = géométrie de l'entité
        - classe = classe de l'entité
        - probability = probabilité d'appartenance à la classe
    """

    def __init__(self, identity, geometry, classe, probability):
        self.identity = identity
        self.geometry = geometry
        self.classe = classe
        self.probability = probability
