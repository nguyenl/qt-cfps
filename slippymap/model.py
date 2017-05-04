import math
from . import proj
from collections import namedtuple


LatLng = namedtuple('LatLng', ['lat', 'lng'])
Point = namedtuple('Point', ['x', 'y'])
Bounds = namedtuple('Bounds', ['minx', 'miny', 'maxx', 'maxy'])
LatLngBounds = namedtuple('LatLngBounds', ['north', 'east', 'south', 'west'])
TileRecord = namedtuple('TileRecord', ['url', 'point', 'xyz'])
XYZ = namedtuple('XYZ', ['x', 'y', 'z'])

TILE_SIZE = 256.0


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

    def _get_pixel_bounds(self, width, height, center=None):
        '''
        Given the width and height in pixels of the widget, returns
        the pixel bounds in tile coordinates.
        '''
        if not center:
            center = self.get_center_pixel()

        minx = center.x - (width/2)
        maxx = center.x + (width/2)
        miny = center.y - (height/2)
        maxy = center.y + (height/2)
        return Bounds(minx, miny, maxx, maxy)

    def _get_latlng_bounds(self, width, height):
        '''
        Returns the bounds of the current widgets in lat/lng
        '''
        # TODO Fix this. It doesn't work correctly.
        raise Exception("This method doesn't work corerctly")
        pbounds = self._get_pixel_bounds(width, height)
        northwest = proj.pixel_to_latlng(pbounds.miny, pbounds.minx, self.zoom)
        southeast = proj.pixel_to_latlng(pbounds.maxy, pbounds.maxx, self.zoom)
        return LatLngBounds(north=northwest[0], east=southeast[1], south=southeast[0], west=northwest[1])

    def _get_tile_bounds(self, width, height, zoom):
        '''
        Given the width and height of the widget as well as the zoom,
        returns the tile bounds.
        '''
        pbounds = self._get_pixel_bounds(width, height)
        minx = int(math.floor(pbounds.minx / TILE_SIZE))
        maxx = int(math.floor(pbounds.maxx / TILE_SIZE))
        miny = int(math.floor(pbounds.miny / TILE_SIZE))
        maxy = int(math.floor(pbounds.maxy / TILE_SIZE))
        return Bounds(minx, miny, maxx, maxy)

    def get_tiles(self, width, height):
        '''
        Given the pixel width and height, returns all the tiles that
        need to be rendered as well as their pixel locations.
        '''
        tbounds = self._get_tile_bounds(width, height, self.zoom)
        pixel_bounds = self._get_pixel_bounds(width, height)

        def create_tile_record(xtile, ytile, zoom):
            url = self._get_url(math.floor(xtile), math.floor(ytile), zoom)

            # xy in tilespace
            xy = Point(*proj.tile_to_pixel(xtile, ytile))
            x = xy.x - pixel_bounds.minx
            y = xy.y - pixel_bounds.miny
            return TileRecord(url, Point(x, y), XYZ(xtile, ytile, zoom))

        tiles = []
        for x in range(tbounds.minx, tbounds.maxx + 1):
            for y in range(tbounds.miny, tbounds.maxy + 1):
                tiles.append(create_tile_record(x, y, self.zoom))
        return tiles

    def zoom_in(self):
        '''
        Zooms into the map (increases the zoom level)
        '''
        if self.zoom < 10:
            self.zoom += 1

    def zoom_out(self):
        '''
        Zooms out of the map (decreases the zoom level)
        '''
        if self.zoom > 4:
            self.zoom -= 1

    def pan(self, width, height, dx, dy):
        '''
        Pans based on the difference of the pixels.
        '''
        pan_modifier = 2 ** (self.zoom - 1)

        dlat = dy / pan_modifier
        dlng = dx / pan_modifier

        # We lock the panning at the edges of the world (no wrapping, sorry)
        xy = proj.latlng_to_pixel(self.lat - dlat, self.lng - dlng, self.zoom)
        center = Point(*xy)
        bounds = self._get_pixel_bounds(width, height, center)
        max_res = TILE_SIZE * (2 ** self.zoom)

        if (bounds.minx > -180 or dlng > 0) and (bounds.maxx < max_res or dlng < 0):
            self.lng += dlng

        if bounds.miny > 0 and bounds.maxy < max_res:
            self.lat -= dlat

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
