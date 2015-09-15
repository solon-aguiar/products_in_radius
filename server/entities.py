
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
