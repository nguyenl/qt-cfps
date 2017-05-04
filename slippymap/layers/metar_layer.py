from datetime import datetime
import requests

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPoint
from .layer import Layer


HOST = 'https://plan.beta.navcanada.ca/'
API_URL = 'weather/api/layer/metar'

ICON_DIR = "slippymap/icons/{}_s.png"


class MetarLayer(Layer):
    def __init__(self, parent):
        super().__init__(parent)
        self.api = "{}{}".format(HOST, API_URL)
        self.queried = False
        self.data = None
        self.cache = {}

    def _create_query(self):
        bbox = "{},{},{},{}".format(-180, -90, 180, 90)
        dateformat = "%Y-%m-%d %H%M"
        start = datetime.utcnow().strftime(dateformat)
        end = datetime.utcnow().strftime(dateformat)
        payload = {
            "rank": self.parent.model.zoom,
            "bbox": bbox,
            "start": start,
            "end": end,
            "productName": "METAR"
            }

        r = requests.get(self.api, params=payload)
        self.data = r.json()
        return self.data

    def fetch(self):
        self._create_query()

    def _get_pixmap_from_file(self, condition, significant):
        if condition is None:
            condition = "NULL"

        if significant:
            condition = "{}_sigwx".format(condition)
            
        if condition in self.cache:
            return self.cache[condition]
        else:
            icon_dir = ICON_DIR
            path = icon_dir.format(condition)
            pixmap = QPixmap()
            pixmap.load(path)
            self.cache[condition] = pixmap
            return pixmap

    def _paint_data(self):
            width = self.parent.width()
            height = self.parent.height()
            qp = QPainter()
            qp.begin(self.parent)
            for metar in self.data['data']:
                wkt = metar['g']
                point = wkt[6:-1].split()  # Ghetto hack, but I didn't want to import a wkt parser
                lat = float(point[1])
                lng = float(point[0])
                point = self.parent.model.latlng_to_pixel(lat, lng, width, height)
                condition = metar['c']
                significant = metar['sw']
                pixmap = self._get_pixmap_from_file(condition, significant)
                point = QPoint(point.x - 7, point.y + 5)
                qp.drawPixmap(point, pixmap)

            qp.end()

    def paint(self):
        if not self.data:
            self.fetch()

        self._paint_data()
