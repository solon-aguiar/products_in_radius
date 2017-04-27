# -*- coding: utf-8 -*-

import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.geo_location import *
from server.entities import *

class TestGeoLocation:
    def test_converts_coordinates_to_cartesian(self):
        rio_de_janeiro = convert_to_cartesian(-22.9068467,-43.1728965)
        assert rio_de_janeiro == (4279.130728586765,-4014.563655759619,-2462.7620620258867)

        sao_paulo = convert_to_cartesian(-23.550520,-46.6333309)
        assert sao_paulo == (4009.494402594272,-4244.865209823,-2527.993774372088)

    def test_converts_distances(self):
        assert euclidean_distance(360.7) == 361.864876256803

class TestShopLocator:
    close_shop = Shop("close shop",59.33265,18.06061)
    same_location_shop = Shop("same location shop",59.33265,18.06061)
    closer_shop = Shop("shop nearby",59.33265,18.06364)
    further_shop = Shop("far shop",59.35419,18.08681)
    boundary_shop = Shop("shop in the boundary",59.33717,18.06637)

    def test_returns_two_shops_if_they_are_in_the_same_location_within_distance(self):
        locator = ShopLocator([self.close_shop,self.same_location_shop])

        shops = locator.shops_within_distance((59.3341,18.065),350)
        assert len(shops) == 2
        assert shops[0].name == "close shop"
        assert shops[1].name == "same location shop"

    def test_returns_only_shops_within_the_desired_distance(self):
        # 2 in the same location, 1 valid and one outside
        locator = ShopLocator([self.close_shop,self.same_location_shop,self.closer_shop,self.further_shop])
        shops = locator.shops_within_distance((59.3341,18.065),350)

        assert len(shops) == 3
        assert shops[0].name == "close shop"
        assert shops[1].name == "same location shop"
        assert shops[2].name == "shop nearby"

    def test_boundaries(self):
        locator = ShopLocator([self.close_shop,self.same_location_shop,self.closer_shop,self.boundary_shop,self.further_shop])
        shops = locator.shops_within_distance((59.3341,18.065),350)

        assert len(shops) == 4
        assert shops[0].name == "close shop"
        assert shops[1].name == "same location shop"
        assert shops[2].name == "shop nearby"
        assert shops[3].name == "shop in the boundary"


