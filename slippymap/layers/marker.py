from PyQt5.QtGui import QPainter, QColor
from .layer import Layer


class Marker(Layer):
    def __init__(self, parent):
        super().__init__(parent)

    def paint(self):
        width = self.parent.width()
        height = self.parent.height()
        point = self.parent.model.latlng_to_pixel(self.parent.model.lat, self.parent.model.lng, width, height)
        qp = QPainter()
        qp.begin(self.parent)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(point.x, point.y, 10, 10)

        lat = 53.5444
        lng = -113.4909

        point = self.parent.model.latlng_to_pixel(lat, lng, width, height)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(point.x, point.y, 10, 10)
        qp.end()
