from PyQt5.QtWidgets import QGraphicsItem

from effigy.NodeIO import NodeIO

class QNodeSceneNode(QGraphicsItem):
    """Graphical representation of Node"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.IO = []
        """Stores all IO for this Node."""

        self.setFlag(QGraphicsItem.ItemIsMovable)   # Item can be dragged with left-click

        self.addGraphicsItems()
        self.addIO()

    def addIO(self):
        """Add IOs to Node"""
        raise NotImplementedError("This method must be implemented in derived class")

    def addGraphicsItems(self):
        """Add Graphic Items for rendering the node"""
        raise NotImplementedError("This method must be implemented in derived class")

    def boundingRect(self):
        """Define appropriate bounding rect for Node body (necessary for interaction like dragging!)"""
        raise NotImplementedError("This method must be implemented in derived class")

    def paint(self, *__args):
        pass


