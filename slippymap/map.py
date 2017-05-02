from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QPoint, Qt
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
        self.cache = {}
        self.url = tile_url
        self.parent = parent
        self.model = MapModel(tile_url, lat, lng, zoom)

    def _create_image(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            r = requests.get(url, verify=False)
            print(url)
            pixmap = QPixmap()
            pixmap.loadFromData(r.content)
            self.cache[url] = pixmap
            return pixmap

    def paintEvent(self, event):
        tiles = self.model.get_tiles(self.width(), self.height())
        qp = QPainter()

        qp.begin(self)

        for tile in tiles:
            pixmap = self._create_image(tile.url)
            point = QPoint(tile.point.x, tile.point.y)
            qp.drawPixmap(point, pixmap)
            qp.setBrush(QColor(0, 100, 0))
            #qp.drawRect(tile.point.x, tile.point.y, 5, 5)
            qp.drawText(tile.point.x, tile.point.y, "{}".format(tile.xyz))

            
        qp.end()

        point = self.model.latlng_to_pixel(self.model.lat, self.model.lng, self.width(), self.height())
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(point.x, point.y, 10, 10)
        qp.end()

        lat = 53.5444
        lng = -113.4909

        point = self.model.latlng_to_pixel(lat, lng, self.width(), self.height())
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(point.x, point.y, 10, 10)
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
