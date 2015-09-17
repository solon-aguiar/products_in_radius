# -*- coding: utf-8 -*-

from math import radians, cos, sin, sqrt
from scipy.spatial import KDTree

EARTH_RADIUS_IN_KM = 6378.137
SEMI_MINOR_AXIS_IN_KM = 6356.7523142
ESQ = 6.69437999014 * 0.001

# Values are in KM
def convert_to_cartesian(lat,lon):
# Implementation based on https://code.google.com/p/pysatel/source/browse/trunk/pysatel/coord.py
    lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - ESQ * sin(lat))
    x = (EARTH_RADIUS_IN_KM / xi) * cos(lat) * cos(lon)
    y = (EARTH_RADIUS_IN_KM / xi) * cos(lat) * sin(lon)
    z = (EARTH_RADIUS_IN_KM / xi * (1 - ESQ)) * sin(lat)
    return x, y, z

def euclidean_distance(distance):
    return 2 * EARTH_RADIUS_IN_KM * sin(distance / (2 * SEMI_MINOR_AXIS_IN_KM))

class ShopLocator:
    def __init__(self, shops):
        self.location_to_shops = {}
        self.points = []
        for shop in shops:
            location = convert_to_cartesian(shop.lat,shop.lng)
            if location not in self.location_to_shops:
                self.location_to_shops[location] = []
                self.points.append(location) # Do not add same point twice
            self.location_to_shops[location].append(shop)
        self.tree = KDTree(self.points)

    def shops_within_distance(self,center_point,radius):
        center = convert_to_cartesian(center_point[0],center_point[1])
        radius = euclidean_distance(radius/1000.0)
        indexes = self.tree.query_ball_point(center, radius)
        all_shops = [self.location_to_shops[self.points[i]] for i in indexes]
        return [shop for sublist in all_shops for shop in sublist]
