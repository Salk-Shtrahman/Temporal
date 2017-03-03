import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import ctypes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import copy
from multiprocessing import Process, Value, Array
from Grinder import *
import matplotlib.patches as patches
import random

class App(QMainWindow):

    def __init__(self):

        user32 = ctypes.windll.user32
        winWidth = user32.GetSystemMetrics(0)
        winHeight= user32.GetSystemMetrics(1)
        super().__init__()
        self.left = 0
        self.top = 30
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = winWidth
        self.height = winHeight*.45
        self.song_mem=[]
        self.scrollWidth=10
        self.scrollPercent =0
        self.connected=False
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.mainPlot = PlotMain(self)
        self.mainPlot.setMaximumSize(QtCore.QSize(1200, 800))
        self.sidePlot = PlotSide(self)
        self.sidePlot.setMaximumSize(QtCore.QSize(500, 800))

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(200)

        self.ind = 1


        self.setupUi(self)

        self.sessionID.setText("Session :1")
        self.port_Status.setText("Port:")
        self.db_status.setText('SQL(%s): %s'% (sql_status,dbName))

        self.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        #self.sidePlot = QtWidgets.QWidget(self.centralwidget)
        self.sidePlot.setObjectName("sidePlot")
        self.gridLayout.addWidget(self.sidePlot, 0, 2, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 959, 298))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        #self.mainPlot = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.mainPlot.setObjectName("mainPlot")
        self.verticalLayout.addWidget(self.mainPlot)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.horizontalScrollBar.setSingleStep(3)
        self.horizontalScrollBar.setPageStep(100000)
        self.horizontalScrollBar.setSliderPosition(99)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.verticalLayout.addWidget(self.horizontalScrollBar)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.song1 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.song1.setFont(font)
        self.song1.setObjectName("song1")
        self.verticalLayout_2.addWidget(self.song1)
        self.song2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.song2.setFont(font)
        self.song2.setObjectName("song2")
        self.verticalLayout_2.addWidget(self.song2)
        self.song3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.song3.setFont(font)
        self.song3.setObjectName("song3")
        self.verticalLayout_2.addWidget(self.song3)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sessionID = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sessionID.setFont(font)
        self.sessionID.setObjectName("sessionID")
        self.horizontalLayout.addWidget(self.sessionID)
        self.port_Status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.port_Status.setFont(font)
        self.port_Status.setObjectName("port_Status")
        self.horizontalLayout.addWidget(self.port_Status)
        self.db_status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.db_status.setFont(font)
        self.db_status.setObjectName("db_status")
        self.horizontalLayout.addWidget(self.db_status)
        self.timeText = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.timeText.setFont(font)
        self.timeText.setObjectName("timeText")
        self.horizontalLayout.addWidget(self.timeText)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1063, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionInfo)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.horizontalScrollBar.sliderMoved['int'].connect(self.horizontalScrollBar.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.song1.setText(_translate("MainWindow", "N/A"))
        self.song2.setText(_translate("MainWindow", "N/A"))
        self.song3.setText(_translate("MainWindow", "N/A"))
        self.sessionID.setText(_translate("MainWindow", "Session :1"))
        self.port_Status.setText(_translate("MainWindow", "Port:"))
        self.db_status.setText(_translate("MainWindow", "SQL(connected):"))
        self.timeText.setText(_translate("MainWindow", "TIME"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
    def slideVal(self):
        scroll=self.horizontalScrollBar.value()
        print(scroll)
        self.horizontalScrollBar.setPageStep(100*self.scrollWidth/(self.ind-self.scrollWidth))

        self.mainPlot.update_scroll(scroll)

    def update_figure(self):
        SONGDICT={0:'x',1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g'}
        song_alpha=[]
        if not new_stuff.value:
            self.timeText.setText(time.strftime("%Y-%m-%d %H:%M:%S"))

        else:
            new_stuff.value = False


            song = songdump[:]
            for tone in song:
                song_alpha.append(SONGDICT[tone])
            print(song)
            self.song_mem.insert(0,''.join(song_alpha))
            if len(self.song_mem) == 4:
                self.song_mem.pop()
            self.mainPlot.update_figure(self.ind)
            self.sidePlot.update_figure(self.ind)

            self.song1.setText(self.song_mem[0] )
            self.song2.setText(self.song_mem[1] if len(self.song_mem)>1 else "N/A")
            self.song3.setText(self.song_mem[2] if len(self.song_mem) > 2 else "N/A")

            if self.ind+1>=self.scrollWidth and not self.connected:
                print("denny chinito is here")
                self.horizontalScrollBar.sliderMoved['int'].connect(self.slideVal)
                self.connected=True
            elif self.ind>self.scrollWidth and self.connected:
                print("deenah latina is here")
                print(100 * self.scrollWidth / (self.ind - self.scrollWidth))
                self.horizontalScrollBar.setPageStep(100 * self.scrollWidth / (self.ind - self.scrollWidth))
            print("deenah latina is gone")
            self.ind+=1

class PlotMain(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.scrollWidth=parent.scrollWidth
        self.setup()
        self.ind=0
        self.scrollTouched=False

    def setup(self):

        self.ax1 = self.figure.add_subplot(211)
        self.ax1.set_autoscale_on(False)
        self.ax1.set_yticks([-1, 0, 1])
        self.ax1.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax2 = self.figure.add_subplot(212)
        self.ax2.grid(True)
        self.ax2.xaxis.grid(True)
        self.ax2.set_ylim(0, 16)
        self.del_but0 = self.ax2.step(1, 1)


    def update_figure(self,ind):
        self.ind=ind
        # idump = [direction, correct, difficulty]
        # lickdump = event_time
        # songdump = song
        # timestampd = t_zero
        t_zero = timestampd.value

        event_time = lickdump[:]
        direction = dump[0]
        correct = dump[1]
        difficulty = dump[2]

        print("bro watch outtttttttttt")
        # print(event_time)
        # print(dump[:])
        ########################### Update color bar graph

        print(ind)

        # result[1]
        fill = "red" if correct else "green"
        # print(fill)
        # print("made it to 1")
        self.ax1.add_patch(
            patches.Rectangle(
                (ind - 1, -1 if direction == -1 else 0),  # (x,y)
                1,  # width
                0.01 if direction == 0 else 1,  # height
                facecolor=fill,
            )
        )
        #  print("made it to 2")


        #  print("made it to 3")
        ###################### Update difficulty graph
        l_diff.append(difficulty)
        now = time.time()
        #  print("made it to 4")
        # print(list(range(ind+1)), difficulty)
        try:  # get rid of whatever was there
            for dell in self.del_but0:
                #         print(dell)
                dell.remove()
        except TypeError:
            self.del_but0.remove()
        except NameError:
            pass
            #      print("made it to 4.5")
            #  print("made it to 5")
        #  print(list(range(ind + 1)), l_diff)
        #  print(self.del_but0)
        self.del_but0 = self.ax2.step(list(range(ind + 1)), l_diff)
        #print("made it to 5.5")
        if ind<=self.scrollWidth:
            self.ax1.set_xlim(0, ind + 1)
            self.ax2.set_xlim(0, ind + 1)
        else:
            if (not self.scrollTouched) or self.scrollPercent>=95 :
                self.lowerlim=ind+1-self.scrollWidth
                self.upperlim=ind+1
            self.ax1.set_xlim(self.lowerlim, self.upperlim)
            self.ax2.set_xlim(self.lowerlim, self.upperlim)



        #print("made it to 6")
        self.draw()

    def update_scroll(self, scroll):
        self.scrollTouched = True
        self.scrollPercent=scroll
        self.lowerlim = scroll*(self.ind-self.scrollWidth)/99
        print('the scrool percentage is %i',self.scrollPercent)
        self.upperlim = self.lowerlim+self.scrollWidth
        self.ax1.set_xlim(self.lowerlim, self.upperlim)
        self.ax2.set_xlim(self.lowerlim, self.upperlim)
        self.draw()


class PlotSide(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setup()

    def setup(self):
        ### first guy
        print(momom)
        self.ax3 = self.figure.add_subplot(311)
        self.ax3.set_xlim(0, 3)
        self.ax3.set_ylim(-1, 1)
        self.ax3.set_title('Most recent')
        self.ax3.set_yticks([-1, 0, 1])
        self.ax3.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax3.axhline(y=0, color='k')
        ### second guy
        self.ax4 = self.figure.add_subplot(312)
        self.ax4.set_xlim(0, 3)
        self.ax4.set_ylim(-1, 1)
        self.ax4.set_title('Last Trail')
        self.ax4.set_yticks([-1, 0, 1])
        self.ax4.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax4.axhline(y=0, color='k')
        ### third guy
        self.ax5 = self.figure.add_subplot(313)
        self.ax5.set_xlim(0, 3)
        self.ax5.set_ylim(-1, 1)
        self.ax5.set_title('2 Trails Ago')
        self.ax5.set_yticks([-1, 0, 1])
        self.ax5.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax5.axhline(y=0, color='k')
        self.figure.subplots_adjust(hspace=.75)

        temp = patches.Rectangle(
            (1, 1),  # (x,y)
            .01,  # width
            1,  # height
        )
        self.del_but1 = self.ax3.add_patch(copy.copy(temp))
        self.del_but2 = self.ax4.add_patch(copy.copy(temp))
        self.del_but3 = self.ax4.add_patch(copy.copy(temp))

        self.bar_cache = []
    def update_figure(self,ind):
        t_zero = timestampd.value
        song = songdump
        event_time = lickdump[:]
        direction = dump[0]
        correct = dump[1]
        difficulty = dump[2]
       # print(ind)
        print("bro watch innnnnnnnnnn")
        self.ax3.set_title('Most Recent #%d' % ind)
        # print("made it to .05")
        try:  # get rid of whatever was there
            for dell in self.del_but1:
                dell.remove()
                # print("made it to .1")
        except TypeError:
            self.del_but1.remove()
            # print("made it to .2")
        except NameError:
            # print("made it to .3")
            pass
        # print("made it to 1")
        temp = patches.Rectangle(
            (event_time[0], -1 if direction == -1 else 0),  # (x,y)
            .01,  # width
            0 if direction == 0 else 1,  # height
        )
        #    print(temp.get_axes())
        # print("made it to 2")
        self.bar_cache.insert(0, copy.copy(temp))  # load up history list
        # print("made it to 2.5")
        if len(self.bar_cache) == 4:
            self.bar_cache.pop()
            #   print(bar_cache[0].get_axes())
        self.del_but1 = self.ax3.add_patch(temp)  # return delete button
        # print("made it to 3")
        #print(self.del_but2)
        try:  # get rid of whatever was there
            for dell in self.del_but2:
                # print("made it to 3.1")
                dell.remove()
        except TypeError:
            # print("made it to 3.2")
            try:
                # print(self.del_but2)
                self.del_but2.remove()
            except Exception as e:
                print(str(e))
            # print("made it to 3.21")

        except NameError:
            # print("made it to 3.3")
            pass
        # print("made it to 4")

        try:
            inst1 = copy.copy(self.bar_cache[1])
            # print("made it to 4.1")

            # print("made it to 4.2")
            self.del_but2 = self.ax4.add_patch(inst1)
            # print("made it to 4.3")
            self.ax4.set_title('Last Trail #%d' % (ind - 1))
        except IndexError:
            print("312 exception")
            pass;
        # print("made it to 5")

        try:  # get rid of whatever was there
            for dell in self.del_but3:
                dell.remove()
        except TypeError:
            try:
            #    print(self.del_but3)
                self.del_but3.remove()
            except Exception as e:
                print(str(e))
            # print("made it to 3.21")
        except NameError:
            pass

        #print(self.bar_cache)
        try:
            inst2 = copy.copy(self.bar_cache[2])
            # print("made it to 5.1")
            # print(inst2)
            self.del_but3 = self.ax5.add_patch(inst2)
            # print("made it to 5.2")

            self.ax5.set_title('2 Trails Ago #%d' % (ind - 2))
            # print("made it to 5.3")
        except IndexError:
            print("313 exception")
            pass
        time.sleep(0.05)
        self.draw()
        # print("made it to 6")


                #self.draw()

if __name__ == '__main__':
    momom=5
    ind = 1
    l_diff = [0, ]
    event_time = []
    p = Grind()

    dbName='Salk'
    try:
        cnx = mysql.connector.connect(user='dennis', password='rh960615',
                                           host='ssh.dennisren.com',
                                           database=dbName)  # connect to Database
        sql_status = 'Connected'
    except Exception as e:
        sql_status = str(e)
    print(sql_status)
    # sql_status = 'Connected'
    new_stuff = Value('b', False)
    dump = Array('i', range(3))
    timestampd = Value('f', 0.0)
    songdump = Array('i', range(4))
    lickdump = Array('f', range(5))
    time.sleep(2)
    slave = Process(target=Serial_Process, args=( p, dump, lickdump, songdump, timestampd, new_stuff))
    slave.start()



    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
