#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""FICHIER DE """

import gdal, gdalconst
import math
import numpy as np


class Background:
    def __init__(self, reference_point, pixel_sizes, image):
        self.reference_point=reference_point
        self.pixel_sizes=pixel_sizes
        self.image = image


    def crop(self, bbox, margins):
        (i_min, j_min), (i_max, j_max) = [
            (
                (x - self.reference_point[0])/(self.pixel_sizes[0]),
                (y - self.reference_point[1])/(self.pixel_sizes[1])
            )
            for x, y in bbox
        ]
        return self.image[
            math.floor(i_min) - margins[0]: math.ceil(i_max) + margins[0],
            math.floor(j_min) - margins[1]: math.ceil(j_max) + margins[1]
        ]


def read_background(filename):

    return Background()
