from geo_location import convert_to_cartesian

class Shop:
    def __init__(self,shop_id,lat,lng):
        self.shop_id = shop_id
        self.lat = float(lat)
        self.lng = float(lng)
        self.tags = []

    def add_tag(self,tag):
        self.tags.append(tag)

class ProductInShop:
    def __init__(self,shop,title,popularity):
        self.shop = shop
        self.title = title
        self.popularity = popularity

    def location(self):
        return convert_to_cartesian(self.shop.lat, self.shop.lng)
