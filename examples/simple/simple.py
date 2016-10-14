from PyQt5.QtWidgets import QApplication
from effigy import QNodeScene, QNodeSceneNode, QNodeView
import sys

from examples.simple.testnode import TestNode

def main():
    app = QApplication(sys.argv)

    scene = QNodeScene()
    editor = QNodeView(scene)

    scene.addItem(TestNode())

    editor.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
else:
    print("This file is meant to be run, not imported.")
    sys.exit(1)
