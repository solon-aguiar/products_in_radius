# -*- coding: utf-8 -*-

from functools import wraps
from flask import Blueprint, current_app, jsonify, request
from geo_location import EARTH_RADIUS_IN_KM
from parser import *
from shop_locator import *

api = Blueprint('api', __name__)

def data_path():
    return current_app.config['DATA_PATH']

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

def check_params(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        radius = request.args.get("radius")
        if radius == None:
            raise ValueError("Search radius cannot be null")
        radius = int(radius)
        if radius <= 0 or radius >= EARTH_RADIUS_IN_KM * 1000:
            raise ValueError("Invalid value for radius. Supported 0 < radius < 6378137.00")

        latitude = request.args.get("lat")
        if latitude == None:
            raise ValueError("Latitude cannot be null")
        longitude = request.args.get("lng")
        if longitude == None:
            raise ValueError("Longitude cannot be null")

        quantity = request.args.get("quantity")
        if quantity == None:
            raise ValueError("Quantity cannot be null")
        quantity = int(quantity)
        if quantity <= 0 or quantity >= 100:
            raise ValueError("Invalid value for quantity. Supported 0 < quantity < 100")
    return decorated_function

def get_params(request):
    latitude = float(request.args.get("lng"))
    longitude = float(request.args.get("lng"))
    radius = int(request.args.get("lng"))
    quantity = int(request.args.get("lng"))
    tags = request.args.get("lng")

    if tags == None:
        tags = []
    return latitude,longitude,radius,quantity,tags

@api.route('/search', methods=['GET'])
@support_jsonp
@check_params
def search():
    check_params(request)
    distance = euclidean_distance(float(request.args.get("radius"))/1000.0)
    center = convert_to_cartesian(float(request.args.get("lat")),float(request.args.get("lng")))
    products = ShopLocator(Parser(data_path()).parse()).products_within_distance(center,distance)
    print len(products)
    sorted_products = sorted(products, key=lambda product: product.popularity)
    samples = sorted_products[0:10]

    return jsonify({'products': [{"shop":{"lng":product.shop.lng,"lat":product.shop.lat}, "title":product.title,"popularity":product.popularity} for product in samples]})
    #return jsonify({'products': [{"shop":{"lng":18.060,"lat":59.332}, "title":"test","popularity":0.9}]})

