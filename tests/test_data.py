# -*- coding: utf-8 -*-
import os, sys

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.data import *
from server.entities import *

class TestParser:
    def test_reads_all_data(self):
        parser = Parser(root + "/test_data")
        results = parser.parse()

        tags = results[0]
        assert len(tags.values()) == 3
        assert [shop.name for shop in tags["home_office"]] == ["acme","tictail"]
        assert [shop.name for shop in tags["it"]] == ["acme"]
        assert [shop.name for shop in tags["sports"]] == ["tictail"]

        shops = results[1]
        assert [shop.name for shop in shops] == ["acme","tictail"]
        assert [(shop.lat,shop.lng) for shop in shops] == [(59.33265, 18.06061),(59.35419, 18.06364)]
        assert [len(shop.products) for shop in shops] == [2,3]
        assert [product.title for product in shops[0].products] == ["light saber","nerf gun"]
        assert [[product.title for product in shops[0].products] =="flag","soccer ball","darts"]

class TestPopularProductsFinder:
    search_coordinates = (59.3341,18.065)
    search_radius = 350

    def test_returns_the_same_product_if_it_is_popular_in_multiple_shops_winthin_the_search_range(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))
        shop.add_product(Product("harry potter II",0.8))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("harry potter",0.9))

        finder = PopularProductsFinder({},[shop,closer_shop])
        products = finder.most_popular_products(self.search_coordinates,self.search_radius,[],1000)

        assert len(products) == 3
        assert products[0].title == "harry potter"
        assert products[1].title == "harry potter"
        assert products[2].title == "harry potter II"

    def test_limits_the_search_to_the_stores_in_which_the_tags_exist(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))
        shop.add_product(Product("harry potter II",0.8))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("nike tiempo",0.9))

        boundary_shop = Shop("shop in the boundary",59.33717,18.06637)
        boundary_shop.add_product(Product("Game of Thrones",0.1))
        boundary_shop.add_product(Product("Hunger Games",0.3))

        finder = PopularProductsFinder({"books":[shop,boundary_shop],"sports":[closer_shop]},[shop,closer_shop,boundary_shop])

        book_products = finder.most_popular_products(self.search_coordinates,self.search_radius,["books"],1000)
        assert len(book_products) == 4
        assert book_products[0].title == "harry potter"
        assert book_products[1].title == "harry potter II"
        assert book_products[2].title == "Hunger Games"
        assert book_products[3].title == "Game of Thrones"

        sport_products = finder.most_popular_products(self.search_coordinates,self.search_radius,["sports"],1000)
        assert len(sport_products) == 1
        assert sport_products[0].title == "nike tiempo"

        all_products = finder.most_popular_products(self.search_coordinates,self.search_radius,["sports","books"],1000)
        assert len(all_products) == 5

    def test_does_not_return_twice_the_product_from_a_store_if_it_matches_both_tags(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))
        shop.add_product(Product("harry potter II",0.8))
        shop.add_product(Product("Ibrahimovic jersey",0.9))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("nike tiempo",0.9))

        finder = PopularProductsFinder({"books":[shop],"sports":[closer_shop,shop]},[shop,closer_shop])

        products = finder.most_popular_products(self.search_coordinates,self.search_radius,[],1000)
        assert len(products) == 4
        assert products[0].title == "nike tiempo"
        assert products[1].title == "Ibrahimovic jersey"
        assert products[2].title == "harry potter"
        assert products[3].title == "harry potter II"

    def test_only_returns_the_desired_amount_of_products(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.95))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("nike tiempo",0.9))

        finder = PopularProductsFinder({},[shop,closer_shop])

        products = finder.most_popular_products(self.search_coordinates,self.search_radius,[],1)
        assert len(products) == 1
        assert products[0].title == "harry potter"

    def test_does_not_break_if_searched_tags_does_not_exist(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("nike tiempo",0.9))

        finder = PopularProductsFinder({"books":[shop],"sports":[closer_shop,shop]},[shop,closer_shop])

        products = finder.most_popular_products(self.search_coordinates,self.search_radius,["movies"],1000)
        assert len(products) == 0

    def test_discards_a_search_tag_if_it_does_not_exist(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))

        closer_shop = Shop("shop nearby",59.33265,18.06364)
        closer_shop.add_product(Product("nike tiempo",0.9))

        finder = PopularProductsFinder({"books":[shop],"sports":[closer_shop]},[shop,closer_shop])

        products = finder.most_popular_products(self.search_coordinates,self.search_radius,["movies","sports"],1000)
        assert len(products) == 1
        assert products[0].title == "nike tiempo"

    def test_returns_an_empty_list_if_no_products_with_tags_exist_within_the_search_range(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))

        further_shop = Shop("far shop",59.35419,18.08681)
        further_shop.add_product(Product("nike tiempo",0.9))

        finder = PopularProductsFinder({"books":[shop],"sports":[further_shop]},[shop,further_shop])

        products = finder.most_popular_products(self.search_coordinates,self.search_radius,["sports"],1000)
        assert len(products) == 0

    def test_returns_the_products_in_descending_order_of_popularity(self):
        shop = Shop("close shop",59.33265,18.06061)
        shop.add_product(Product("harry potter",0.9))
        shop.add_product(Product("harry potter II",0.8))
        shop.add_product(Product("Ibrahimovic jersey",0.7))

        finder = PopularProductsFinder({"books":[shop],"sports":[shop]},[shop])

        products = finder.most_popular_products(self.search_coordinates,1000,[],2)
        assert len(products) == 2
        assert products[0].title == "harry potter"
        assert products[1].title == "harry potter II"

