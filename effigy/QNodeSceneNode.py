from PyQt5.QtWidgets import QGraphicsItem

import uuid

from effigy.NodeIO import NodeIO


class QNodeSceneNode(QGraphicsItem):
    """Graphical representation of Node"""

    # Here we define some information about the node
    author = "DrLuke"       # Author of this node (only used for namespacing, never visible to users)
    modulename = "builtin"  # Internal name of the module, make this something distinguishable
    name = "Basenode"       # Human-readable name

    placeable = False       # Whether or not this node should be placeable from within the editor
    Category = ["Builtin"]     # Nested categories this Node should be sorted in

    # Description, similar to python docstrings (Brief summary on first line followed by a long description)
    description = """This node is the base class for all nodes.
It should never be placeable in the editor. However if you DO see this in the editor, something went wrong!"""

    def __init__(self, deserializedata=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.IO = [] # Stores all IO for this Node

        self.id = uuid.uuid4().int

        self.setFlag(QGraphicsItem.ItemIsMovable)   # Item can be dragged with left-click

        if deserializedata is not None:
            self.deserializeinternal(deserializedata)
        else:
            self.addGraphicsItems()
            self.addIO()

        self.serializeinternal()

    def serializeinternal(self):
        """Builtin internal node serializer, shouldn't be called from outside"""
        # Things to serialize: Node position
        # Node Links
        # Node UUID
        # Object type
        serdata = {}    # Contains serialized data of this object
        serdata["pos"] = [self.pos().x(), self.pos().y()]
        serdata["uuid"] = self.id
        serdata["type"] = str(type(self).author + "." + type(self).modulename + "." + type(self).__name__)
        serdata["io"] = {}
        for io in self.IO:
            serdata["io"][io.name] = {}
            serdata["io"][io.name]["links"] = []
            for nodeLink in io.nodeLinks:
                serdata["io"][io.name]["links"].append([nodeLink.startIO.id, nodeLink.endIO.id])



        print(serdata)


    def deserializeinternal(self):
        """Builtin internal node deserializer, shouldn't be called from outside"""
        pass


    def serialize(self):
        """Custom node serializer, can be used to serialize non-default parameters"""
        raise NotImplementedError("This method must be implemented in derived class")

    def deserialize(self, data):
        """Custom node deserializer, restores node state with non-default parameters"""
        raise NotImplementedError("This method must be implemented in derived class")

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

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        for IO in self.IO:
            for link in IO.nodeLinks:
                link.updateBezier()

        super().mouseMoveEvent(QGraphicsSceneMouseEvent)


