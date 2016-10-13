from PyQt5.QtWidgets import QGraphicsItem

import enum
import uuid


class NodeIODirection(enum):
    """Establish if IO direction is input, output or any"""
    any = 0
    output = 1
    input = 2

class NodeIOMultiplicity(enum):
    """Whether the node can be connected to multiple other nodes, or just one"""
    single = 0
    multiple = 1

class NodeIO:
    """General Input and Output class for Node links.

    This class builds the basis for inputs and outputs for nodes. You link nodes together via those inputs and outputs,
    and all IO must be typed. Only compatible IO (that is, IO of same type) can be linked together. Compatibility is
    established with the 'isinstance' method. Each IO has a direction, i.e. input, output or any. Inputs may only be
    conected with inputs (and 'any' of course), and vice versa."""

    # Direction for this class
    classDirection = NodeIODirection.Any
    # Multiplicity for this class
    classMultiplicity = NodeIOMultiplicity.multiple

    def __init__(self, iotype):
        if type(iotype) is not type:
            raise TypeError("iotype argument is of type '%s', but must be of type 'type'." % type(iotype))
        self.iotype = iotype
        self.iodirection = NodeIO.classDirection
        self.id = uuid.uuid4().int  # Unique ID to identify node across multiple sessions.

class NodeInput(NodeIO):
    """General Input and Output class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.input
    classMultiplicity = NodeIOMultiplicity.multiple

class QNodeSceneNode(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)




