#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""FICHIER DE TRAITEMENT DES IMAGES EN ARRIERE PLAN"""

import gdal
import gdalconst

import math
import numpy as np


class Background:
    def __init__(self, reference_point, pixel_sizes, image):
        self.reference_point = reference_point
        self.pixel_sizes = pixel_sizes
        self.image = image

    def get_crop_points(self, bbox):
        return [
            (
                (y - self.reference_point[1])/self.pixel_sizes[1],
                (x - self.reference_point[0])/self.pixel_sizes[0]
            )
            for x, y in bbox
        ]

    def crop(self, bbox, margins):
        (i_max, j_min), (i_min, j_max) = get_crop_points(self, bbox)
        return np.transpose(
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


def read_background(filename):
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    Ox, px, _, Oy, _, py = dataset.GetGeoTransform()
    return Background(
        (Ox, Oy),
        (px, py),
        [
            dataset.GetRasterBand(band).ReadAsArray()
            for band in range(1, dataset.RasterCount + 1)
        ]
    )
