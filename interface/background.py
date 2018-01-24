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
        (i_max, j_min), (i_min, j_max) = [
            (
                (y - self.reference_point[1])/self.pixel_sizes[1],
                (x - self.reference_point[0])/self.pixel_sizes[0]
            )
            for x, y in bbox
        ]
        print(i_min, i_max, j_min, j_max)
        return np.transpose(
            np.swapaxes(
                np.array(
                    [
                        band[
                            math.floor(i_min) - margins[1]:math.ceil(i_max) + margins[1],
                            math.floor(j_min) - margins[0]:math.ceil(j_max) + margins[0]
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
