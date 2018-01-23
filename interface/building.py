#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""FICHIER DE DEFINITION DE LA CLASSE BATIMENT"""


import os

import shapefile


class Building:
    """
    Building class

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


def read_building(directory, building_id, classe, probability):
    return Building(
        building_id,
        get_geometry(os.path.join(directory, str(building_id) + '.shp')),
        classe,
        probability
    )


def get_geometry(building_path):
    return [
        polygon.points
        for polygon in shapefile.Reader(building_path).shapes()
    ]
