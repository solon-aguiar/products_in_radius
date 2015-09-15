# -*- coding: utf-8 -*-

import csv
from entities import *

class Parser:
    PRODUCTS_FILE = "products.csv"
    SHOPS_FILE = "shops.csv"
    TAGGINGS_FILE = "taggings.csv"
    TAGS_FILE = "tags.csv"

    def __init__(self,files_directory):
        self.files_directory = files_directory

    def parse(self):
        tags = {}
        tags_file = csv.DictReader(open(self.absolute_path(self.TAGS_FILE)))
        for tag in tags_file:
            tags[tag["id"]] = tag["tag"]

        shops = {}
        shops_file = csv.DictReader(open(self.absolute_path(self.SHOPS_FILE)))
        for shop in shops_file:
            shops[shop["id"]] = Shop(shop["id"],shop["lat"],shop["lng"])

        taggings_file = csv.DictReader(open(self.absolute_path(self.TAGGINGS_FILE)))
        for tagging in taggings_file:
            shops[tagging["shop_id"]].add_tag(tags[tagging["tag_id"]])

        products_file = csv.DictReader(open(self.absolute_path(self.PRODUCTS_FILE)))
        return [ProductInShop(shops[product["shop_id"]],product["title"],float(product["popularity"])) for product in products_file]

    def absolute_path(self,file_path):
        return u"%s/%s" % (self.files_directory, file_path)
