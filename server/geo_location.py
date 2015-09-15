from math import radians, cos, sin, sqrt

A = 6378.137
B = 6356.7523142
ESQ = 6.69437999014 * 0.001

def convert_to_cartesian(lat,lng):
    lat, lon = radians(lat), radians(lng)
    xi = sqrt(1 - ESQ * sin(lat))
    x = (A / xi) * cos(lat) * cos(lon)
    y = (A / xi) * cos(lat) * sin(lon)
    z = (A / xi * (1 - ESQ)) * sin(lat)
    return x, y, z

def euclidean_distance(distance):
    return 2 * A * sin(distance / (2 * B))
