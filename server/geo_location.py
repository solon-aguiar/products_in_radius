from math import radians, cos, sin, sqrt

EARTH_RADIUS_IN_KM = 6378.137
SEMI_MINOR_AXIS_IN_KM = 6356.7523142
FLATENNING_FACTOR = 6.69437999014 * 0.001

# Values are in KM
def convert_to_cartesian(lat,lon):
    lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - FLATENNING_FACTOR * sin(lat))
    x = (EARTH_RADIUS_IN_KM / xi) * cos(lat) * cos(lon)
    y = (EARTH_RADIUS_IN_KM / xi) * cos(lat) * sin(lon)
    z = (EARTH_RADIUS_IN_KM / xi * (1 - FLATENNING_FACTOR)) * sin(lat)
    return x, y, z

def euclidean_distance(distance):
    return 2 * EARTH_RADIUS_IN_KM * sin(distance / (2 * SEMI_MINOR_AXIS_IN_KM))
