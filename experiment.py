import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Example(QWidget):

   def __init__(self):
      super(Example, self).__init__()
      self.initUI()

   def initUI(self):
      vbox = QVBoxLayout(self)
      hbox = QHBoxLayout()
      self.l1 = QLabel("Drag scrollbar sliders to change color")
      self.l1.setFont(QFont("Arial",16))

      hbox.addWidget(self.l1)
      self.s1 = QScrollBar()
      self.s1.setMaximum(255)

      self.s1.sliderMoved.connect(self.sliderval)
      self.s2 = QScrollBar()
      self.s2.setMaximum(255)
      self.s2.sliderMoved.connect(self.sliderval)

      self.s3 = QScrollBar()
      self.s3.setMaximum(255)
      self.s3.sliderMoved.connect(self.sliderval)

      hbox.addWidget(self.s1)
      hbox.addWidget(self.s2)
      hbox.addWidget(self.s3)

      self.setGeometry(300, 300, 300, 200)
      self.setWindowTitle('QSplitter demo')
      self.show()

   def sliderval(self):
      print (self.s1.value(),self.s2.value(), self.s3.value())
      palette = QPalette()
      c = QColor(self.s1.value(),self.s2.value(), self.s3.value(),255)
      palette.setColor(QPalette.Foreground,c)
      self.l1.setPalette(palette)

def main():
   app = QApplication(sys.argv)
   ex = Example()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()