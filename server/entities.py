
class Shop:
    def __init__(self,name,lat,lng):
        self.lat = float(lat)
        self.lng = float(lng)
        self.name = name
        self.products = []

    def add_product(self,product):
        self.products.append(product)

class Product:
    def __init__(self,title,popularity):
        self.title = title
        self.popularity = popularity

class ProductInShop:
    def __init__(self,lat,lng,popularity,title):
        self.title = title
        self.popularity = popularity
        self.lat = lat
        self.lng = lng
