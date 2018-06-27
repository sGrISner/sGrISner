#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    `Model` module
    ==============
    This module assembles the model functionnalities in the MVC paradigm.

    `Background`
    ---------------------
    Defines a class to deal with backgrounds. For now, it works only with
    orthoimages.

    `Building`
    ---------------------
    Defines a class to deal with instances, namely buildings. For now, it reads
    only shapefiles.
"""

__docformat__ = 'reStructuredText'


import math
import os
import fnmatch
import functools

import numpy as np
import qimage2ndarray
import shapely

import PyQt5.QtGui
import PyQt5.QtCore

from geo2d import GeoShape, GeoRaster



def to_qimage(georaster):
    return qimage2ndarray.array2qimage(
        georaster.image
    )


def to_qpixmap(georaster):
    return PyQt5.QtGui.QPixmap.fromImage(
        to_qimage(georaster)
    )


class Background:
    """
        Manages background for the building.
    """

    def __init__(self, directory, extension='.geotiff'):
        """
            Initiate Building class.

            :param identity: building identity
            :type identity: string
            :param geometry: building geometry
            :type geometry: list
            :param labels: building labels
            :type labels: string
            :param probabilities: building labels probabilities
            :type probabilities: float
        """
        self.background_infos = {
            os.path.join(directory, filename):
            GeoRaster.geo_info(os.path.join(directory, filename))
            for filename in fnmatch.filter(
                os.listdir(directory),
                '*' + extension
            )
        }
    
    def crop(self, bbox, margins):
        return functools.reduce(
            lambda lhs, rhs: lhs.union(rhs),
            [
                GeoRaster.GeoRaster.from_file(
                    ortho,
                    dtype=np.uint8
                ).crop(
                    GeoRaster.add_margins(
                        bbox,
                        ortho_res,
                        margins
                    )
                )
                for ortho, (ortho_bbox, ortho_res) in self.background_infos.items()
                if GeoRaster.overlap(
                    GeoRaster.add_margins(
                        bbox,
                        ortho_res,
                        margins
                    ),
                    ortho_bbox
                )
            ]
        )

class Building:
    """
        Building to show and annotate.

        Attribute `identity` stores the building identity.
        Attribute `geometry` stores the building geometry.
        Attribute `labels` stores the building class or labels.
        Attribute `probabilities` stores the building class probabilities.
    """

    def __init__(self, identity='', shape=GeoShape.GeoShape(), labels=[], probabilities=[], scores=[]):
        """
            Initiate Building class.

            :param identity: building identity
            :type identity: string
            :param shape: building shape
            :type shape: GeoShape.GeoShape
            :param labels: building labels
            :type labels: string
            :param probabilities: building labels probabilities
            :type probabilities: float
            :param scores: building labels scores
            :type scores: int
        """
        self.shape = shape

        self.identity = identity
        self.labels = labels
        self.probabilities = probabilities
        self.scores = scores if scores else len(probabilities) * [10]

    @staticmethod
    def read(directory, building_id, labels, probabilities, scores):
        """
            Create Building from file in `directory`.
            :param directory: directory path
            :type directory: string
            :param building_id: building identity
            :type building_id: string
            :param labels: building labels
            :type labels: string
            :param probabilities: building labels probabilities
            :type probabilities: float
            :return: Building object
            :rtype: Building
        """
        return Building(
            building_id,
            GeoShape.GeoShape.from_file(
                os.path.join(
                    directory, str(building_id) + '.shp'
                )
            ),
            labels,
            probabilities,
            scores
        )

    def to_qgeometry(self, background, margins):
        (x_min, _), (_, y_max) = self.shape.bbox
        return [
            PyQt5.QtGui.QPolygonF(
                [
                    PyQt5.QtCore.QPointF(
                        (x_min - x) / background.pixel_sizes[1] + margins[0],
                        (y_max - y) / background.pixel_sizes[0] + margins[1]
                    )
                    for x, y in polygon.exterior.coords
                ]
            )
            for polygon in self.shape.geometry
        ]

    def find_background(self, background, margins):
        return to_qpixmap(
            background.crop(
                self.shape.bbox,
                margins
            )
        )
