from scipy.spatial import KDTree
from geo_location import *

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
