from datetime import datetime
import requests

from PyQt5.QtGui import QPainter, QColor
from .layer import Layer


HOST = 'https://plan.beta.navcanada.ca/'
API_URL = 'weather/api/layer/site'


class SiteLayer(Layer):
    def __init__(self, parent):
        super().__init__(parent)
        self.api = "{}{}".format(HOST, API_URL)
        self.queried = False
        self.data = None

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
            "productName": "SITE"
            }

        r = requests.get(self.api, params=payload)
        self.data = r.json()
        return self.data

    def fetch(self):
        self._create_query()

    def _paint_data(self):
            width = self.parent.width()
            height = self.parent.height()
            qp = QPainter()
            qp.begin(self.parent)

            if self.parent.model.is_night:
                qp.setPen(QColor(200, 200, 200))
                qp.setBrush(QColor(200, 200, 200))
            else:
                qp.setPen(QColor(0, 0, 0))                
                qp.setBrush(QColor(0, 0, 0))

            for site in self.data['data']:
                wkt = site['g']
                point = wkt[6:-1].split()  # Ghetto hack, but I didn't want to import a wkt parser
                lat = float(point[1])
                lng = float(point[0])
                point = self.parent.model.latlng_to_pixel(lat, lng, width, height)

                qp.drawRect(point.x - 1, point.y - 1, 3, 3)
                qp.drawText(point.x + 5, point.y, site['a'])

            qp.end()

    def paint(self):
        if not self.data:
            self.fetch()

        self._paint_data()
