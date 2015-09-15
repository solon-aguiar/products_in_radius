from scipy.spatial import KDTree

class ProductShopLocator:
    def __init__(self, products):
        self.location_to_product = {}
        self.points = []
        for product in products:
            location = product.location()
            if location not in self.location_to_product:
                self.location_to_product[location] = []
            self.location_to_product[location].append(product)
            self.points.append(location)
        self.tree = KDTree(self.points)

    def products_within_distance(self, center_point, radius):
        indexes = self.tree.query_ball_point(center_point, radius)
        products = [self.location_to_product[self.points[i]] for i in indexes]
        return [product for sublist in products for product in sublist]
