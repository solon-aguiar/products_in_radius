# -*- coding: utf-8 -*-

import csv
from entities import *
from shop_locator import *
from sets import Set

class Parser:
    PRODUCTS_FILE = "products.csv"
    SHOPS_FILE = "shops.csv"
    TAGGINGS_FILE = "taggings.csv"
    TAGS_FILE = "tags.csv"

    def __init__(self,files_directory):
        self.files_directory = files_directory

    def parse(self):
        tags_mapping = {}

        tags = {}
        tags_file = csv.DictReader(open(self.absolute_path(self.TAGS_FILE)))
        for tag in tags_file:
            tags[tag["id"]] = tag["tag"]
            tags_mapping[tag["tag"]] = []

        shops = {}
        shops_file = csv.DictReader(open(self.absolute_path(self.SHOPS_FILE)))
        for shop in shops_file:
            shops[shop["id"]] = Shop(shop["name"],shop["lat"],shop["lng"])

        taggings_file = csv.DictReader(open(self.absolute_path(self.TAGGINGS_FILE)))
        for tagging in taggings_file:
            tags_mapping[tags[tagging["tag_id"]]].append(shops[tagging["shop_id"]])

        products_file = csv.DictReader(open(self.absolute_path(self.PRODUCTS_FILE)))
        for product in products_file:
            shops[product["shop_id"]].add_product(Product(product["title"],product["popularity"]))
        return (tags_mapping,shops.values())

    def absolute_path(self,file_path):
        return u"%s/%s" % (self.files_directory, file_path)

class PopularProductsFinder:
    def __init__(self,tags_to_shops,shops):
        self.tags_mapping = tags_to_shops
        self.shops = shops
        self.complete_locator = ShopLocator(shops)

    def most_popular_products(self,center,radius,tags,quantity):
        tree = self.complete_locator
        if len(tags) != 0:
            shops = self.get_all_shops(tags)
            if len(shops) == 0:
                return []
            tree = ShopLocator(shops)
        shops = tree.shops_within_distance(center,radius)
        return self.filter_products_in_shops(shops,quantity)

    def filter_products_in_shops(self,shops,quantity):
        products = []
        for shop in shops:
            for product in shop.products:
                products.append(ProductInShop(shop.lat,shop.lng,product.popularity,product.title))
        most_popular = sorted(products,key=lambda product:product.popularity)[0:quantity]
        most_popular.reverse()
        return most_popular

    def get_all_shops(self,tags):
        shops = []
        for tag in tags:
            if self.tags_mapping.has_key(tag):
                shops.append(self.tags_mapping[tag])
        return Set([shop for sublist in shops for shop in sublist]) #Set removes the duplicates

