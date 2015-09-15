# -*- coding: utf-8 -*-
import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.parser import Parser

class TestParser:
    def test_reads_all_data(self):
        parser = Parser(root + "/test_data")
        results = parser.parse()

        tags = results[0]
        assert len(tags.values()) == 2
        assert [shop.name for shop in tags["home_office"]] == ["acme","tictail"]
        assert [shop.name for shop in tags["it"]] == ["acme"]

        shops = results[1]
        assert [shop.name for shop in shops] == ["acme","tictail"]
        assert [(shop.lat,shop.lng) for shop in shops] == [(1,0),(2,1)]
        assert [len(shop.products) for shop in shops] == [2,3]
        assert [product.title for product in shops[0].products] == ["light saber","nerf gun"]
        assert [[product.title for product in shops[0].products] =="flag","soccer ball","darts"]

