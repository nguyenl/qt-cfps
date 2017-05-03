from PyQt5.QtGui import QPainter, QColor
from .layer import Layer


class TileNames(Layer):
    '''
    A layer that draws text over the xyz location of the tiles.
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.model = self.parent.model

    def paint(self):
        width = self.parent.width()
        height = self.parent.height()
        tiles = self.model.get_tiles(width, height)
        qp = QPainter()
        qp.begin(self.parent)
        for tile in tiles:
            qp.setBrush(QColor(0, 100, 0))
            qp.drawText(tile.point.x, tile.point.y, "{}".format(tile.xyz))
        qp.end()
