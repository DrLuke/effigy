from effigy import QNodeSceneNode, NodeIO, NodeInput, NodeOutput

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QPen, QColor, QBrush

class TestNode(QNodeSceneNode):
    author = "Luke"
    modulename = "testmod"
    name = "Example Node"

    def addIO(self):
        newnode = NodeOutput(str, parent=self, name="output")
        newnode.setPos(20, 10)
        self.IO.append(newnode)

        newnode = NodeInput(str, parent=self, name="input")
        newnode.setPos(-20, 10)
        self.IO.append(newnode)

    def boundingRect(self):
        return self.mainRect.rect()

    def addGraphicsItems(self):
        self.mainRect = QGraphicsRectItem(QRectF(-15, -15, 30, 30), self)

    def selectedChanged(self, state):
        if state:
            self.mainRect.setPen(QPen(Qt.red))
        else:
            self.mainRect.setPen(QPen(Qt.black))
