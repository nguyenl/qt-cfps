import math
from .projection import project_to_tilespace, unproject_from_tilespace


def pixel_to_latlng(x, y, zoom):
    xtile = x / 256.0
    ytile = y / 256.0
    return unproject_from_tilespace(xtile, ytile, zoom)


def latlng_to_pixel(lat, lng, zoom):
    xtile, ytile = project_to_tilespace(lat, lng, zoom)
    return xtile * 256, ytile * 256


def tile_to_pixel(xtile, ytile):
    x = math.floor(xtile) * 256
    y = math.floor(ytile) * 256
    return x, y


def latlng_to_tile(lat, lng, zoom):
    xtile, ytile = project_to_tilespace(lat, lng, zoom)
    return math.floor(xtile), math.floor(ytile)
