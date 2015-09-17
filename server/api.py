# -*- coding: utf-8 -*-

from functools import wraps
from flask import Blueprint, current_app, jsonify, request
from geo_location import convert_to_cartesian, euclidean_distance
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

@api.route('/search', methods=['GET'])
@support_jsonp
def search():
    print request
    distance = euclidean_distance(float(request.args.get("radius"))/1000.0)
    center = convert_to_cartesian(float(request.args.get("lat")),float(request.args.get("lng")))
    products = ShopLocator(Parser(data_path()).parse()).products_within_distance(center,distance)
    print len(products)
    sorted_products = sorted(products, key=lambda product: product.popularity)
    samples = sorted_products[0:10]

    return jsonify({'products': [{"shop":{"lng":product.shop.lng,"lat":product.shop.lat}, "title":product.title,"popularity":product.popularity} for product in samples]})
    #return jsonify({'products': [{"shop":{"lng":18.060,"lat":59.332}, "title":"test","popularity":0.9}]})

