# -*- coding: utf-8 -*-

import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.geo_location import *

class TestGeoLocation:
    def test_converts_coordinates_to_cartesian(self):
        rio_de_janeiro = convert_to_cartesian(-22.9068467,-43.1728965)
        assert rio_de_janeiro == (4279.130728586765,-4014.563655759619,-2462.7620620258867)

        sao_paulo = convert_to_cartesian(-23.550520,-46.6333309)
        assert sao_paulo == (4009.494402594272,-4244.865209823,-2527.993774372088)

    def test_converts_distances(self):
        assert euclidean_distance(360.7) == 361.864876256803
