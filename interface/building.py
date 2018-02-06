#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" FICHIER DE DEFINITION DE LA CLASSE BATIMENT """

import os

import shapefile


class Building:
    """
    BUILDING CLASS

    ATTRIBUTS :
    ===========
        - identity = identifiant de l'entité.
        - geometry = géométrie de l'entité.
        - classe = classe de l'entité.
        - probability = probabilité d'appartenance à la classe.

    METHODES:
    ==========
        - get_bounding_box: retourne les 2 extrémités de la géométrie.
        - get_points: retourne les sommets des géométries.
    """

    def __init__(self, identity, geometry, classe, probability):
        self.identity = identity
        self.geometry = geometry
        self.classe = classe
        self.probability = probability

    def get_bounding_box(self):
        X, Y = zip(
            *self.get_points()
        )
        return [(min(X), min(Y)), (max(X), max(Y))]

    def get_points(self):
        pts = []
        for polygon in self.geometry:
            pts += [point for point in polygon]
        return pts


def read_building(directory, building_id, classe, probability):
    """Lecture de la géométrie et création d'un objet Building"""
    return Building(
        building_id,
        get_geometry(os.path.join(directory, str(building_id) + '.shp')),
        classe,
        probability
    )


def get_geometry(building_path):
    """Retourne tous les sommets des polygones d'un fichier SHP"""
    return [
        polygon.points
        for polygon in shapefile.Reader(building_path).shapes()
    ]
