from effigy import QNodeSceneNode, NodeIO, NodeInput, NodeOutput

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QColor, QBrush

class TestNode(QNodeSceneNode):
    def addIO(self):
        self.IO.append(NodeInput(str, self))

    def boundingRect(self):
        return self.mainRect.rect()

    def addGraphicsItems(self):
        self.mainRect = QGraphicsRectItem(QRectF(-5, -5, 10, 10), self)
