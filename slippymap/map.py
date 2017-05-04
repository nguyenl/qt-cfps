from collections import OrderedDict
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .layers.marker import Marker
from .layers.tile_names import TileNames
from .layers.tile_layer import TileLayer
from .layers.site_layer import SiteLayer
from .layers.metar_layer import MetarLayer
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
        self.mouse_down = False
        self._init_layers()

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        if angle > 0:
            self.model.zoom_in()
        else:
            self.model.zoom_out()
        #self._fetch_layers()
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.mouse_down = True
            self._update_mouse_pos(event)

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.mouse_down = False
            self.repaint()

    def mouseMoveEvent(self, event):
        """
        Pan the map if the mouse is down.
        """
        if self.mouse_down:
            dx = self.last_x - event.x()
            dy = self.last_y - event.y()
            self._update_mouse_pos(event)
            self.model.pan(self.width(), self.height(), dx, dy)
            self.repaint()

    def get_layer(self, layername):
        return self.layers[layername]

    def _update_mouse_pos(self, event):
        self.last_x = event.x()
        self.last_y = event.y()

    def _init_layers(self):
        '''
        Initializes the layer classes.
        '''
        self.layers = OrderedDict()
        self.layers['base'] = TileLayer(self)
        #self.layers['marker'] = Marker(self)
        #self.layers['tilenames'] = TileNames(self)

        self.layers['site'] = SiteLayer(self)
        self.layers['metar'] = MetarLayer(self)
        self.fetch_layers()

    def fetch_layers(self):
        if self.layers['site'].enabled:
            self.layers['site'].fetch()
        if self.layers['metar'].enabled:
            self.layers['metar'].fetch()

    def _draw_layers(self):
        for name, layer in self.layers.items():
            if layer.enabled:
                layer.paint()

    def _update_status_bar(self):
        self.parent.statusBar().clearMessage()
        message = "Center: {} {}  Zoom: {}".format(self.model.lat, self.model.lng, self.model.zoom)
        self.parent.statusBar().showMessage(message)

    def paintEvent(self, event):
        self._draw_layers()
        self._update_status_bar()
