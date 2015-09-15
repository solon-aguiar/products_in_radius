# -*- coding: utf-8 -*-

from functools import wraps
from flask import Blueprint, current_app, jsonify, request

api = Blueprint('api', __name__)

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

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)

@api.route('/search', methods=['GET'])
@support_jsonp
def search():
    print data_path('shops.csv')
    return jsonify({'products': [{"shop":{"lng":18.060,"lat":59.332}, "title":"test","popularity":0.9}]})
