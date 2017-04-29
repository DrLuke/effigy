from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QUndoCommand

from enum import Enum
import uuid

from effigy.NodeLink import NodeLink, InvalidLinkException

class NodeIODirection(Enum):
    """Establish if IO direction is input, output or any"""
    any = 0
    output = 1
    input = 2

class NodeIOMultiplicity(Enum):
    """Whether the node can be connected to multiple other nodes, or just one"""
    single = 0
    multiple = 1

class NodeIO(QGraphicsItem):
    """General Input and Output class for Node links.

    This class builds the basis for inputs and outputs for nodes. You link nodes together via those inputs and outputs,
    and all IO must be typed. Only compatible IO (that is, IO of same type) can be linked together. Compatibility is
    established with the 'isinstance' method. Each IO has a direction, i.e. input, output or any. Inputs may only be
    conected with inputs (and 'any' of course), and vice versa."""

    # Direction for this class
    classDirection = NodeIODirection.any
    # Multiplicity for this class
    classMultiplicity = NodeIOMultiplicity.multiple

    class LinkUndoCommand(QUndoCommand):
        def __init__(self, startIO, endIO, scene, *args, **kwargs):
            self.startIO = startIO
            self.endIO = endIO
            self.scene = scene

            self.link = None
            
            super().__init__(*args, **kwargs)

        def redo(self):
            self.link = NodeLink(startIO=self.startIO, endIO=self.endIO)
            self.link.updateBezier()

            self.scene.addItem(self.link)

        def undo(self):
            self.startIO.deleteLink(self.link)
            self.link = None

    def __init__(self, iotype, name, displaystr=None, *args, **kwargs):
        if type(iotype) is not type:
            raise TypeError("iotype argument is of type '%s', but must be of type 'type'." % type(iotype))

        super().__init__(*args, **kwargs)

        self.iotype = iotype
        self.iodirection = NodeIO.classDirection
        self.id = uuid.uuid4().int  # Unique ID to identify node across multiple sessions.

        self.name = str(name)   # Each IO needs a name unique across all instances of the node class using it
        self.displaystring = displaystr     # Preferred String to display next to IO when rendering. Not required for it to work.

        self.addGraphicsItems()

        self.nodeLinks = []
        self.tempNodeLink = None

    # Define a bounding rect for collision detection (needed for interacting with the IO)
    def boundingRect(self):
        return self.backgroundItem.rect()

    def addGraphicsItems(self):
        """Add Items to draw the IO pin. Can be overridden for custom graphics"""
        self.backgroundItem = QGraphicsRectItem(QRectF(-5, -5, 10, 10), self)

    def paint(self, *__args):
        """Must be defined, but as this is just a container item, it doesn't actually paint anything."""
        pass

    def deleteLink(self, link):
        link.startIO.nodeLinks.remove(link)
        link.endIO.nodeLinks.remove(link)
        self.scene().removeItem(link)

    def recursiveIOCheck(self, item):
        """Recursively check if item is a child of an IO item"""
        if item is None:  # We reached the topmost item
            return None
        if isinstance(item, NodeIO):  # Found a NodeIO
            return item
        else:
            return self.recursiveIOCheck(item.parentItem())  # We must go deeper and deeper!

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if type(self).classMultiplicity == NodeIOMultiplicity.single:
            for link in self.nodeLinks:
                self.deleteLink(link)
        if self.tempNodeLink is not None:
            pass    # TODO: Throw exception? Can this realistically ever happen?
        else:
            if self.classDirection == NodeIODirection.input:
                # On inputs, io is the ending point of bezier curve
                self.tempNodeLink = NodeLink(startIO=None, endIO=self)
            else:
                # Everywhere else, io is start point of bezier curve
                self.tempNodeLink = NodeLink(startIO=self, endIO=None)
            self.scene().addItem(self.tempNodeLink)


    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        # update temporary link
        if self.tempNodeLink is not None:
            if self.classDirection == NodeIODirection.input:
                self.tempNodeLink.updateBezier(overrideStartpos=QGraphicsSceneMouseEvent.scenePos())
            else:
                self.tempNodeLink.updateBezier(overrideEndpos=QGraphicsSceneMouseEvent.scenePos())

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        if self.tempNodeLink is None:
            return

        #  Delete temporary link
        self.scene().removeItem(self.tempNodeLink)
        self.tempNodeLink = None

        # Try to find any item at end coordinates
        endpos = QGraphicsSceneMouseEvent.scenePos()
        itematendpos = self.scene().itemAt(endpos, QTransform())

        # Check if item is nodeIO
        enditem = self.recursiveIOCheck(itematendpos)
        if enditem is not None:
            try:
                # Check if IO directions are compatible
                if self.classDirection == enditem.classDirection and not self.classDirection == NodeIODirection.any and not enditem.classDirection == NodeIODirection.any:
                    raise InvalidLinkException
                if self.classDirection == NodeIODirection.input:
                    # On inputs, io is the ending point of bezier curve
                    linkAction = type(self).LinkUndoCommand(startIO=enditem, endIO=self, scene=self.scene())
                    self.scene().undostack.push(linkAction)
                else:
                    # Everywhere else, io is start point of bezier curve
                    linkAction = type(self).LinkUndoCommand(startIO=self, endIO=enditem, scene=self.scene())
                    self.scene().undostack.push(linkAction)


            except InvalidLinkException:
                pass



class NodeInput(NodeIO):
    """General Input class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.input
    classMultiplicity = NodeIOMultiplicity.multiple

class NodeOutput(NodeIO):
    """General Output class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.output
    classMultiplicity = NodeIOMultiplicity.single
