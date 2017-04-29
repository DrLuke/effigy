from PyQt5.QtWidgets import QGraphicsScene, QUndoStack


class QNodeScene(QGraphicsScene):
    def __init__(self, *__args):
        self.undostack = QUndoStack()

        super().__init__(*__args)

    def keyPressEvent(self, event):
        if event.text() == "a":
            self.undostack.undo()
        else:
            self.undostack.redo()