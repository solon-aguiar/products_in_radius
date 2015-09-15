# -*- coding: utf-8 -*-
import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.parser import Parser

class TestParser:
    def test_reads_all_data(self):
        parser = Parser(root + "/test_data")
        products = parser.parse()

        assert len(products) == 5
        assert ["light saber","flag","soccer ball","darts","nerf gun"] == [product.title for product in products]
        assert [0.9,0.7,0.33,0.6,0.95] == [product.popularity for product in products]


