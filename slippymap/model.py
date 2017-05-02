import math
from . import proj
from collections import namedtuple


LatLng = namedtuple('LatLng', ['lat', 'lng'])
Point = namedtuple('Point', ['x', 'y'])
Bounds = namedtuple('Bounds', ['minx', 'miny', 'maxx', 'maxy'])
LatLngBounds = namedtuple('LatLngBounds', ['north', 'east', 'south', 'west'])
TileRecord = namedtuple('TileRecord', ['url', 'point', 'xyz'])


class MapModel:
    '''
    Stores the state of the map widget.
    '''
    def __init__(self, tile_url, lat, lng, zoom):
        self._lng = lng
        self._lat = lat
        self._zoom = zoom
        self.tile_url = tile_url

    def latlng_to_pixel(self, lat, lng, width, height):
        bounds = self._get_pixel_bounds(width, height)
        xy = proj.latlng_to_pixel(lat, lng, self.zoom)
        x = xy[0] - bounds.minx
        y = xy[1] - bounds.miny
        return Point(x, y)

    def get_center_pixel(self):
        center = proj.latlng_to_pixel(self.lat, self.lng, self.zoom)
        return Point(*center)

    def _get_url(self, x, y, z):
        return self.tile_url.format(z, x, y)

    def _get_pixel_bounds(self, width, height):
        '''
        Given the width and height in pixels of the widget, returns
        the pixel bounds in tile coordinates.
        '''
        center = self.get_center_pixel()

        minx = center.x - (width/2)
        maxx = center.x + (width/2)
        miny = center.y - (height/2)
        maxy = center.y + (height/2)
        return Bounds(minx, miny, maxx, maxy)

    def _get_latlng_bounds(self, width, height, zoom):
        '''
        Given the height and width of the pixels of the widget,
        returns the latlng bounds.
        '''
        pbounds = self._get_pixel_bounds(width, height)
        northwest = proj.pixel_to_latlng(pbounds.miny, pbounds.minx, zoom)
        southeast = proj.pixel_to_latlng(pbounds.maxy, pbounds.maxx, zoom)
        return LatLngBounds(north=northwest[0], east=southeast[1], south=southeast[0], west=northwest[1])
        
    def get_tiles(self, width, height):
        '''
        Given the pixel width and height, returns all the tiles that
        need to be rendered as well as their pixel locations.
        '''
        print("width: {}  height: {}".format(width, height))
        bounds = self._get_latlng_bounds(width, height, self.zoom)
        pixel_bounds = self._get_pixel_bounds(width, height)
        print(bounds)
        print(pixel_bounds)

        def create_tile_record(xtile, ytile, zoom):
            url = self._get_url(math.floor(xtile), math.floor(ytile), zoom)

            # xy in tilespace
            xy = Point(*proj.tile_to_pixel(xtile, ytile))
            x = xy.x - pixel_bounds.minx
            y = xy.y - pixel_bounds.miny
            return TileRecord(url, Point(x, y), (xtile, ytile, zoom))

        tl = proj.latlng_to_tile(bounds.north, bounds.west, self.zoom)
        br = proj.latlng_to_tile(bounds.south, bounds.east, self.zoom)
        tiles = []
        for x in range(tl[0] - 1, br[0] + 1):
            for y in range(tl[1], br[1] + 2):
                tiles.append(create_tile_record(x, y, self.zoom))
        return tiles

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def lng(self):
        return self._lng

    @lng.setter
    def lng(self, value):
        self._lng = value

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
