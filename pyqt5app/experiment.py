import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        layout = QVBoxLayout(self)
        mapper = QSignalMapper(self)

        for i in range(5):

            button = QPushButton()
            button.setText("Button " + str(i))
            button.clicked.connect(mapper.map)
            if i % 2 == 0:
                mapper.setMapping(button, str(i))
            else:
                mapper.setMapping(button, i)
            layout.addWidget(button)

        mapper.mapped['QString'].connect(self.stringMapped)
        mapper.mapped[int].connect(self.intMapped)

    def stringMapped(self, value):

        print
        "stringMapped", value

    def intMapped(self, value):

        print
        "intMapped", value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
