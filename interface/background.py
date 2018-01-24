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

    def crop(self, bbox, margins):
        print(bbox)
        (i_min, j_min), (i_max, j_max) = [
            (
                (x - self.reference_point[0])/(self.pixel_sizes[0]),
                (y - self.reference_point[1])/(-self.pixel_sizes[1])
            )
            for x, y in bbox
        ]

        print(self.reference_point[0],self.reference_point[1])
        print(i_min, j_min, i_max, j_max)
        print(math.ceil(i_max),math.ceil(j_max))
        return np.swapaxes(
            np.array(
                [
                    band[
                        math.floor(j_max) - margins[0]:math.ceil(j_min) + margins[0],
                        math.floor(i_min) - margins[1]:math.ceil(i_max) + margins[1]
                    ]
                    for band in self.image
                ]
            ),
            0,
            2
        )


def read_background(filename):
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    Ox, px, _, Oy, _, py = dataset.GetGeoTransform()
    return Background(
        (Ox, Oy),
        (px, -py),
        [dataset.GetRasterBand(band).ReadAsArray() for band in range(1, dataset.RasterCount + 1)]
    )
