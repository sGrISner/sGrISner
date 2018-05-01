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

import PyQt5.QtGui
import PyQt5.QtCore

from geo2d import GeoShape, GeoRaster

import qimage2ndarray


class Background(GeoRaster.GeoRaster):
    """
        Canvas background.

        Attribute `reference_point` stores the reference point.
        Attribute `pixel_sizes` stores the horizontal and vertical resolutions.
        Attribute `image` stores the matrix image.
    """

    def __init__(self, reference_point, pixel_sizes, image):
        """
            Extend `GeoRaster` to initiate `Background`.
            :param reference_point: reference point
            :type reference_point: tuple
            :param pixel_sizes: pixel resolutions
            :type pixel_sizes: tuple
            :param image: 3d image matrix
            :type image: np.array
        """
        super().__init__(reference_point, pixel_sizes, image)

    def to_qimage(self):
        return qimage2ndarray.array2qimage(
            self.image
        )

    def to_qpixmap(self):
        return PyQt5.QtGui.QPixmap.fromImage(
            self.to_qimage()
        )

class Building(GeoShape.GeoShape):
    """
        Building to show and annotate.

        Attribute `identity` stores the building identity.
        Attribute `geometry` stores the building geometry.
        Attribute `labels` stores the building class or labels.
        Attribute `probabilities` stores the building class probabilities.
    """

    def __init__(self, identity, geometry, labels, probabilities):
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
        super().__init__(geometry)

        self.identity = identity
        self.labels = labels
        self.probabilities = probabilities

    @classmethod
    def from_file(cls, directory, building_id, labels, probabilities):
        """
            Create Building `cls` from file in `directory`.
            :param directory: directory path
            :type directory: string
            :param building_id: building identity
            :type building_id: string
            :param labels: building labels
            :type labels: string
            :param probabilities: building labels probabilities
            :type probabilities: float
            :return: cls
            :rtype: Building
        """
        cls = super().from_file(
            os.path.join(
                directory, str(building_id) + '.shp'
            )
        )
        cls.identity = building_id
        cls.labels = labels
        cls.probabilities = probabilities
        return cls

    def to_qgeometry(self, background, margins):
        (x_min, y_min), (x_max, y_max) = self.get_bounding_box()
        dx, dy = background.get_translation(
            [(x_min, y_min), (x_max, y_max)],
            margins
        )
        return [
            PyQt5.QtGui.QPolygonF(
                [
                    PyQt5.QtCore.QPointF(
                        (x_min - x) / background.pixel_sizes[1] + margins[0],
                        (y_max - y) / background.pixel_sizes[0] + margins[1]
                    )
                    for x, y in polygon
                ]
            ).translated(dx, dy)
            for polygon in self.geometry
        ]
