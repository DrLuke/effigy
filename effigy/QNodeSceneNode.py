from PyQt5.QtWidgets import QGraphicsItem, QUndoCommand

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
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

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

    def selectedChanged(self, state):
        """React to being (de-)selected with visual cues"""
        raise NotImplementedError("This method must be implemented in derived class")

    def paint(self, *__args):
        pass

    class moveCommand(QUndoCommand):
        def __init__(self, item, newPos, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.selectedItems = set([x for x in item.scene().selectedItems() if issubclass(type(x), QNodeSceneNode)])
            self.positions = {}

            for iteritem in self.selectedItems:
                    self.positions[iteritem.id] = [iteritem, None, None]

            self.positions[item.id] = [item, item.pos(), newPos]

            self.firstredo = True

        def redo(self):
            if not self.firstredo:
                for position in self.positions.values():
                    if position[2] is not None:
                        position[0].setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)  # Disable, or it will generate a move command
                        position[0].setPos(position[2])
                        position[0].setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
                        position[0].updateLinkGraphics()  # Update links
            else:
                self.firstredo = False  # Workaround, because the action already happens somewhere else when the command is created

        def undo(self):
            for position in self.positions.values():
                if position[1] is not None:
                    position[0].setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)  # Disable, or it will generate a move command
                    position[0].setPos(position[1])
                    position[0].setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
                    position[0].updateLinkGraphics()  # Update links

        def id(self):
            return 1

        def mergeWith(self, command):
            # Merge command with this
            # Note: 'command' is a newer command than this
            if command.selectedItems == self.selectedItems:
                for item in self.selectedItems:
                    # Take start position from older command, and new position from newer command if it isn't None
                    oldpos = self.positions[item.id][1] if self.positions[item.id][1] is not None else command.positions[item.id][1]
                    # Take end position from newest command
                    newpos = command.positions[item.id][2] if command.positions[item.id][2] is not None else self.positions[item.id][2]
                    self.positions[item.id] = [self.positions[item.id][0], oldpos, newpos]
                return True # Indicate success
            else:
                return False

    def updateLinkGraphics(self):
        for IO in self.IO:
            for link in IO.nodeLinks:
                link.updateBezier()

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        super().mouseMoveEvent(QGraphicsSceneMouseEvent)

    def mouseDownEvent(selfs, QGraphicsSceneMouseEvent):
        pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            move = QNodeSceneNode.moveCommand(self, value)
            self.scene().undostack.push(move)

        elif change == QGraphicsItem.ItemPositionHasChanged:
            self.updateLinkGraphics()

        elif change == QGraphicsItem.ItemSelectedHasChanged:
            self.selectedChanged(value)

        return super().itemChange(change, value)


