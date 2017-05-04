from .layer import Layer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPoint
import requests


TILE_DIR = "slippymap/tiles/base/{}/{}/{}.png"
NIGHT_TILE_DIR = "slippymap/tiles/night/{}/{}/{}.png"


class TileLayer(Layer):
    '''
    A layer to draw slippy map tiles.
    '''
    def __init__(self, parent, url=None):
        super().__init__(parent)
        self.url = url
        self.tile_dir = TILE_DIR
        self.model = parent.model
        self.cache = {}

    def night_action_event(self, use_night):
        if use_night:
            self.tile_dir = NIGHT_TILE_DIR
        else:
            self.tile_dir = TILE_DIR

    def _get_tile_pixmap(self, tile):
        if self.url:
            return self._get_pixmap_from_url(tile.url)
        else:
            return self._get_pixmap_from_file(tile.xyz)

    def _get_pixmap_from_file(self, xyz):
        path = self.tile_dir.format(xyz.z, xyz.x, xyz.y)
        pixmap = QPixmap()
        pixmap.load(path)
        return pixmap

    def _get_pixmap_from_url(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            r = requests.get(url, verify=False)
            pixmap = QPixmap()
            pixmap.loadFromData(r.content)
            self.cache[url] = pixmap
            return pixmap

    def _draw_tiles(self):
        tiles = self.model.get_tiles(self.parent.width(), self.parent.height())
        qp = QPainter()

        qp.begin(self.parent)
        for tile in tiles:
            pixmap = self._get_tile_pixmap(tile)
            point = QPoint(tile.point.x, tile.point.y)
            qp.drawPixmap(point, pixmap)
        qp.end()

    def paint(self):
        self._draw_tiles()
