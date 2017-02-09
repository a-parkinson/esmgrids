#!/usr/bin/env python

from __future__ import print_function

import sys
import numpy as np
import netCDF4 as nc
from .regular_grid import RegularGrid

class T42Grid(RegularGrid):

    def __init__(self, num_lons, num_lats, num_levels, mask_file=None, description=''):

        levels = range(num_levels)

        self.type = 'Spectral'

        if mask_file:
            with nc.Dataset(mask_file) as f:
                try:
                    mask = np.round(f.variables['WGOCN'][0, 0, :, :-1])
                except KeyError as e:
                    print("Error: var WGOCN not in {}.".format(mask_file),
                           file=sys.stderr)
                    raise e
        else:
            mask = np.ones((num_lats, num_lons))

        assert mask.shape[0] == num_lats
        assert mask.shape[1] == num_lons

        super(T42Grid, self).__init__(num_lons, num_lats, mask_t=mask,
                                      levles=levels, description=description)