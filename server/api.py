# -*- coding: utf-8 -*-

from functools import wraps
from flask import Blueprint, current_app, jsonify, request
from geo_location import EARTH_RADIUS_IN_KM, ShopLocator
from data import *

api = Blueprint('api', __name__)
finder = None
MAXIMUM_QUANTITY = 100

def data_path():
    return current_app.config['DATA_PATH']

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
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
        if quantity <= 0 or quantity >= MAXIMUM_QUANTITY:
            raise ValueError("Invalid value for quantity. Supported 0 < quantity < 100")
        return f(*args, **kwargs)
    return decorated_function

def get_params(request):
    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lng"))
    radius = int(request.args.get("radius"))
    quantity = int(request.args.get("quantity"))
    tags_args = request.args.get("tags")
    tags = []

    if tags_args != None:
        if str(tags_args).strip() == "":
            tags = []
        else:
            tags = str(tags_args).split(",")

    return (latitude,longitude),radius,quantity,tags

def finder():
    if current_app.config['FINDER'] == None:
        tags_mapping,shops = Parser(data_path()).parse()
        current_app.config['FINDER'] = PopularProductsFinder(tags_mapping,shops)
    return current_app.config['FINDER']

@api.route('/search', methods=['GET'])
@support_jsonp
@check_params
def search():
    center,radius,quantity,tags = get_params(request)
    products = finder().most_popular_products(center,radius,tags,quantity)
    return jsonify({'products': [{"shop":{"lng":product.lng,"lat":product.lat}, "title":product.title,"popularity":product.popularity} for product in products]})

