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


import georasters as gr

import shapefile

import math
import numpy as np


import PyQt5.QtGui
import PyQt5.QtCore
import qimage2ndarray

import os


class Background:
    """
        Canvas background.

        Attribute `reference_point` stores the reference point.
        Attribute `pixel_sizes` stores the horizontal and vertical resolutions.
        Attribute `image` stores the matrix image.
    """

    def __init__(self, reference_point, pixel_sizes, image):
        """
            Initiate Background class.

            :param reference_point: reference point
            :type reference_point: tuple
            :param pixel_sizes: pixel resolutions
            :type pixel_sizes: tuple
            :param image: 3d image matrix
            :type image: np.array
        """
        self.reference_point = reference_point
        self.pixel_sizes = pixel_sizes
        self.image = image

    @classmethod
    def from_file(cls, filename):
        """
            Create Background `cls` from file in `filname`.

            :param filename: file path
            :type filename: string
            :return: cls
            :rtype: Background
        """
        data = gr.from_file(filename)
        Ox, px, _, Oy, _, py = data.geot
        return cls(
            (Ox, Oy),
            (px, py),
            np.moveaxis(data.raster.data, 0, -1)
        )

    def get_crop_points(self, bbox):
        """
            Get crop points in coordinates in image.

            :param bbox: bounding box
            :type bbox: list
            :return: extremal points defining the crop region
            :rtype: list
        """
        return [
            (
                (y - self.reference_point[1])/self.pixel_sizes[1],
                (x - self.reference_point[0])/self.pixel_sizes[0]
            )
            for x, y in bbox
        ]

    def get_translation(self, bbox, margins):
        """
            Get translation if crop points are outside image.

            :param bbox: bounding box
            :type bbox: list
            :param margins: crop margins
            :type margins: tuple
            :return: vertical and horizontal translation
            :rtype: tuple
        """
        (i_max, j_min), (i_min, j_max) = self.get_crop_points(bbox)
        return [
            max(-l_min, 0) - max(l_max - self.image.shape[0], 0)
            for l_min, l_max in [(j_min, j_max), (i_min, i_max)]
        ]

    def crop(self, bbox, margins):
        """
            Crop the corresponding matrix to the bounding box and the defined
            margins.

            :param bbox: bounding box
            :type bbox: list
            :param margins: crop margins
            :type margins: tuple
            :return: 3d croped image matrix
            :rtype: np.array
        """
        (i_max, j_min), (i_min, j_max) = self. get_crop_points(bbox)
        (pi_min, pi_max), (pj_min, pj_max) = [
            (
                max(math.floor(l_min) - margins[1], 0),
                min(math.ceil(l_max) + margins[1], self.image.shape[0])
            )
            for l_min, l_max in [(i_min, i_max), (j_min, j_max)]
        ]
        return PyQt5.QtGui.QPixmap.fromImage(
            qimage2ndarray.array2qimage(
                self.image[pi_min: pi_max, pj_min: pj_max, :]
            )
        )


class Building:
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
        self.identity = identity
        self.geometry = geometry
        self.labels = labels
        self.probabilities = probabilities

    @classmethod
    def from_shapefile(cls, directory, building_id, labels, probabilities):
        """
            Create Building `cls` from shapefile in `directory`.

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
        return cls(
            building_id,
            [
                polygon.points
                for polygon in shapefile.Reader(
                    os.path.join(directory, str(building_id) + '.shp')
                ).shapes()
            ],
            labels,
            probabilities
        )

    def get_qgeometry(self, background, margins):
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

    def get_bounding_box(self):
        """
            Get building bounding box.

            :return: bounding box rectangle
            :rtype: list
        """
        X, Y = zip(
            *self.get_points()
        )
        return [(min(X), min(Y)), (max(X), max(Y))]

    def get_points(self):
        """
            Get all building points.

            :return: all points
            :rtype: list
        """
        return [point for polygon in self.geometry for point in polygon]
