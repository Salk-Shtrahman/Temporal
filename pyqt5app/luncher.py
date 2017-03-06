import os
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        # create objects
        self.pb = QPushButton(self.tr("Run command"))
        self.te = QTextEdit()

        # layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.pb)
        layout.addWidget(self.te)
        self.setLayout(layout)

        # create connection
        self.pb.clicked[bool].connect(self.run_command)

    def run_command(self):
        stdouterr = os.popen4("dir")[1].read()
        self.te.setText(stdouterr)

if __name__ == "__main__":
    main()
