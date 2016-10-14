from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QRectF

from enum import Enum
import uuid


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

    def __init__(self, iotype, *__args):
        super().__init__(*__args)
        if type(iotype) is not type:
            raise TypeError("iotype argument is of type '%s', but must be of type 'type'." % type(iotype))
        self.iotype = iotype
        self.iodirection = NodeIO.classDirection
        self.id = uuid.uuid4().int  # Unique ID to identify node across multiple sessions.

    # Define a bounding rect for collision detection (needed for interacting with the IO)
    # TODO: Make this skinnable!
    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)

    def addGraphicsItems(self):
        """Add Items to draw the IO pin. Can be overridden for custom graphics"""
        self.backgroundItem = QGraphicsRectItem(QRectF(-5, -5, 10, 10))

    def link(self, linkIO):
        pass

    def paint(self, *__args):
        pass

class NodeInput(NodeIO):
    """General Input class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.input
    classMultiplicity = NodeIOMultiplicity.multiple

class NodeOutput(NodeIO):
    """General Output class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.output
    classMultiplicity = NodeIOMultiplicity.single
