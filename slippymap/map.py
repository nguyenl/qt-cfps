from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPoint
import requests
from .model import MapModel


class Map(QWidget):
    '''
    A Slippy map tile QT Widget.
    '''
    def __init__(self, tile_url, lat, lng, zoom, parent):
        '''
        Constructs the map widget.

            Args:
                tile_url: The slippy map tile URL to use.
                lat: The initial latitude to display.
                lng: The initial longitude
                zoom: The initial zoom level
                parent: The Parent QWidget for this widget.
        '''
        super().__init__(parent)
        self.url = tile_url
        self.parent = parent
        self.model = MapModel(tile_url, lat, lng, zoom)

    def _create_image(self, url):
        print(url)
        r = requests.get(url)
        r.content
        pixmap = QPixmap()
        pixmap.loadFromData(r.content)
        return pixmap

    def paintEvent(self, event):
        tiles = self.model.get_tiles(self.width(), self.height())
        for tile in tiles:
            pixmap = self._create_image(tile.url)
            qp = QPainter()
            qp.begin(self)
            point = QPoint(tile.point.x, tile.point.y)
            qp.drawPixmap(point, pixmap)
            qp.end()
            

            
        # x, y = tiles.latlng_to_pixel(self.model.lat, self.model.lng, self.model.zoom)
        # tx, ty = tiles.pixels_to_tile(x, y, self.model.zoom)

        # print(x, y, self.model.zoom)
        # image = self._create_image(tx, ty, self.model.zoom)

        # qp = QPainter()
        # qp.begin(self)
        # point = QPoint(0, 0)
        # qp.drawPixmap(point, image)
        # qp.end()
