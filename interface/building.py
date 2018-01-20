#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os

from osgeo import ogr

""" - FICHIER DE DEFINITION DE LA CLASSE BATIMENT - """

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
        get_geometry(directory + str(building_id) + '.gml', 'GML'),
        classe,
        probability
    )


def get_geometry(building_path, driver_name):
    source = ogr.GetDriverByName(driver_name).Open(building_path, 0)
    if source is None:
        raise IOError('Could not open ' + building_path)
    else:
        return [feature.GetGeometryRef() for feature in source.GetLayer()]
