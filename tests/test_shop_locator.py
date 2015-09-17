# -*- coding: utf-8 -*-

import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.shop_locator import ShopLocator
from server.entities import *

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


