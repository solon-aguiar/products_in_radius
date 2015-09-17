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
