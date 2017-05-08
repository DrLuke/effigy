from PyQt5.QtWidgets import QApplication
from effigy import QNodeScene, QNodeSceneNode, QNodeView
import sys

from examples.simple.testnode import TestNode

def customexcepthook(type, value, traceback):
    print(traceback.print_exc())
    raise(Exception())
sys.excepthook = customexcepthook

def main():
    app = QApplication(sys.argv)

    scene = QNodeScene()
    editor = QNodeView(scene)

    a = TestNode()
    b = TestNode()
    c = TestNode()

    scene.addItem(a)
    scene.addItem(b)
    scene.addItem(c)

    editor.show()

    ret = app.exec_()

    print("EXITING:")
    foo = a.serializeinternal()
    a.deserializeinternal(foo)
    b.serializeinternal()
    c.serializeinternal()

    return ret

if __name__ == "__main__":
    sys.exit(main())
else:
    print("This file is meant to be run, not imported.")
    sys.exit(1)
