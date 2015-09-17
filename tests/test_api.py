# -*- coding: utf-8 -*-

from conftest import *

def test_returns_error_if_any_of_the_required_parameters_are_missing(client):
     with pytest.raises(ValueError) as error:
         client.get("/search?")
     assert str(error.value) == "Search radius cannot be null"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=1")
     assert str(error.value) == "Latitude cannot be null"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=1&lat=56.180")
     assert str(error.value) == "Longitude cannot be null"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=1&lat=56.180&lng=18.080")
     assert str(error.value) == "Quantity cannot be null"

def test_returns_error_if_input_values_are_invalid(client):
     with pytest.raises(ValueError) as error:
         client.get("/search?radius=1&lat=56.180&lng=18.080&quantity=-1")
     assert str(error.value) == "Invalid value for quantity. Supported 0 < quantity < 100"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=1&lat=56.180&lng=18.080&quantity=100")
     assert str(error.value) == "Invalid value for quantity. Supported 0 < quantity < 100"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=-1&lat=56.180&lng=18.080&quantity=1")
     assert str(error.value) == "Invalid value for radius. Supported 0 < radius < 6378137.00"

     with pytest.raises(ValueError) as error:
         client.get("/search?radius=6378138&lat=56.180&lng=18.080&quantity=10")
     assert str(error.value) == "Invalid value for radius. Supported 0 < radius < 6378137.00"

def test_returns_a_list_of_products_and_its_locations(client):
    response = client.get("/search?radius=350&lat=59.3341&lng=18.065&quantity=10&&tags=home_office")
    assert {'products': [{'popularity': '0.95', 'shop': {'lat': 59.33265, 'lng': 18.06061}, 'title': 'nerf gun'}, {'popularity': '0.9', 'shop': {'lat': 59.33265, 'lng': 18.06061}, 'title': 'light saber'}]} == response.json

    another_response = client.get("/search?radius=350&lat=59.3341&lng=18.065&quantity=10&&tags=sports")
    assert {'products': []} == another_response.json

    another_response = client.get("/search?radius=350&lat=59.3341&lng=18.065&quantity=10&&tags=home_office,sports")
    assert {'products': [{'popularity': '0.95', 'shop': {'lat': 59.33265, 'lng': 18.06061}, 'title': 'nerf gun'}, {'popularity': '0.9', 'shop': {'lat': 59.33265, 'lng': 18.06061}, 'title': 'light saber'}]} == response.json

