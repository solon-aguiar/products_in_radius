from scipy.spatial import KDTree
from geo_location import convert_to_cartesian

class ProductShopLocator:
    def __init__(self, shops):
        self.location_to_shop = {}
        self.points = []
        for shop in products:
            location = convert_to_cartesian(shop.lat,shop.lng)
            if location not in self.location_to_product:
                self.location_to_product[location] = []
            self.location_to_product[location].append(shop)
            self.points.append(location)
        self.tree = KDTree(self.points)

    def products_within_distance(self,center_point,radius):
        center = convert_to_cartesian(center_point)
        radius = euclidean_distance(radius)
        indexes = self.tree.query_ball_point(center, radius)
        products = [self.location_to_product[self.points[i]] for i in indexes]
        return [shop for sublist in products for shop in sublist]
