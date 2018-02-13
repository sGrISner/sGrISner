#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ``Background`` module.
    ======================

    Defines a class to deal with backgrounds. For now, it works only with
    orthoimages.
"""

__docformat__ = 'reStructuredText'


import gdal
import gdalconst

import math
import numpy as np


import PyQt5.QtGui

import qimage2ndarray


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
    def from_geotiff(cls, filename):
        """
            Create Background `cls` from geotiff in `filname`.

            :param filename: geotiff path
            :type filename: string
            :return: cls
            :rtype: Background
        """
        dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
        Ox, px, _, Oy, _, py = dataset.GetGeoTransform()
        return cls(
            (Ox, Oy),
            (px, py),
            [
                dataset.GetRasterBand(band).ReadAsArray()
                for band in range(1, dataset.RasterCount + 1)
            ]
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

        return PyQt5.QtGui.QPixmap.fromImage(
            qimage2ndarray.array2qimage(
                np.transpose(
                    np.swapaxes(
                        np.array(
                            [
                                band[
                                    max(math.floor(i_min) - margins[1], 0):min(math.ceil(i_max) + margins[1], band.shape[0]),
                                    max(math.floor(j_min) - margins[0], 0):min(math.ceil(j_max) + margins[0], band.shape[1])
                                ]
                                for band in self.image
                            ]
                        ),
                        0,
                        2
                    ),
                    (1, 0, 2)
                )
            )
        )
