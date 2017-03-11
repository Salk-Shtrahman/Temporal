import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
import csv
import ctypes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import copy
from multiprocessing import Process, Value, Array, Manager
from Grinder import *
import matplotlib.patches as patches
import random
import signal, time
import os
from luncher import Luncher
from settings import Settings
class App(QMainWindow):

    def __init__(self,cnx):

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
        self.cnx=cnx
        self.cursor = self.cnx.cursor()

        self.writer=csv.writer(prep.theFile)
        self.flushButtonStatus=True
        ###########Obtain Session ID from Server

        self.cursor.execute(
            "INSERT INTO  Temporal_Session (Animal_ID, Training, Punishment_Duration, Tone_Duration, Ttime_Between_Tones, Lickwindow_Duration, R_Opentime, L_Opentime, Trial_Limit, min_Difficulty, max_Difficulty, Drip_Delay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (config[0], config[1], config[2], config[3], config[4], config[5], config[6], config[7], config[8],
             config[9], config[10], config[11]))
        self.cnx.commit()
        read_que = '''
            SELECT
            Temporal_Session.id
            FROM
            Temporal_Session
            ORDER BY Temporal_Session.id DESC
            LIMIT 1
        '''
        self.cursor.execute(read_que)

        self.session_ID = self.cursor.fetchone()[0] #get first shit of tuple

        #########################################

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

        self.sessionID.setText("Session : %i"% self.session_ID)
        self.port_Status.setText("Port: %s"%prep.portName )
        self.db_status.setText('SQL(%s): %s'% (prep.sql_status,dbName))
        self.quitButton.clicked.connect(self.close)

        self.flushButton.setIcon(QtGui.QIcon('flushOff.png'))
        self.flushButton.setIconSize(QtCore.QSize(75,75))
        self.flushButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon);
        self.flushButton.clicked.connect(self.flushValves)

        self.startButton.setIcon(QtGui.QIcon('play.png'))
        self.startButton.setIconSize(QtCore.QSize(75, 75))
        self.pauseButton.setIcon(QtGui.QIcon('pause.png'))
        self.pauseButton.setIconSize(QtCore.QSize(75, 75))
        self.statusbar.showMessage(prep.pathName)

        self.actionSettings.triggered.connect(self.openSettings)
        self.show()
        # time.sleep(3)
        # self.update_figure()
        #
        # time.sleep(3)
        # self.update_figure()
        # time.sleep(3)
        # self.update_figure()
    def openSettings(self):
        #send pause signal
        #wait for confirmed pause

        self.settingsWindow = Settings("COM4")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1063, 394)
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
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 2, 1, 1)
        # self.sidePlot = QtWidgets.QWidget(self.centralwidget)
        self.sidePlot.setObjectName("sidePlot")
        self.gridLayout.addWidget(self.sidePlot, 0, 3, 1, 1)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 871, 289))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        # self.mainPlot = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.mainPlot.setObjectName("mainPlot")
        self.verticalLayout.addWidget(self.mainPlot)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.horizontalScrollBar.setSingleStep(3)
        self.horizontalScrollBar.setPageStep(50)
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
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 5, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)
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
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_2.addWidget(self.line_4, 2, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.verticalLayout_3.addWidget(self.startButton)
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setObjectName("pauseButton")
        self.verticalLayout_3.addWidget(self.pauseButton)
        self.flushButton = QtWidgets.QToolButton(self.centralwidget)
        self.flushButton.setObjectName("flushButton")
        self.verticalLayout_3.addWidget(self.flushButton)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 2, 3, 1, 1)
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setObjectName("quitButton")
        self.gridLayout_2.addWidget(self.quitButton, 0, 3, 1, 1)
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
        # self.startButton.setText(_translate("MainWindow", "Start"))
        # self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.flushButton.setText(_translate("MainWindow", "Flush"))
        self.quitButton.setText(_translate("MainWindow", "Quit n Save"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))

    def slideVal(self):
        scroll=self.horizontalScrollBar.value()
        print(scroll)
        self.horizontalScrollBar.setPageStep(100*self.scrollWidth/(self.ind-self.scrollWidth))

        self.mainPlot.update_scroll(scroll)
    def flushValves(self):
        if self.flushButtonStatus:
            self.flushButton.setIcon(QtGui.QIcon('flushOn.png'))
            self.flushButton.setText('Stop Flush')
        else:
            self.flushButton.setIcon(QtGui.QIcon('flushOff.png'))
            self.flushButton.setText('Flush')
        self.flushButtonStatus= not self.flushButtonStatus

    def update_figure(self):
        SONGDICT={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G'}
        song_alpha=[]
        if not new_stuff.value:
            self.timeText.setText(time.strftime("%Y-%m-%d %H:%M:%S"))

        else:
            new_stuff.value = False


            song = songdump[:]
            for tone in song:
                song_alpha.append(SONGDICT[tone])
            # print(song)
            self.song_mem.insert(0,''.join(song_alpha))
            if len(self.song_mem) == 4:
                self.song_mem.pop()
            self.mainPlot.update_figure(self.ind)
            self.sidePlot.update_figure(self.ind)
            self.writeSQL()
            self.writeCSV()


            self.song1.setText(self.song_mem[0] )
            self.song2.setText(self.song_mem[1] if len(self.song_mem)>1 else "N/A")
            self.song3.setText(self.song_mem[2] if len(self.song_mem) > 2 else "N/A")

            if self.ind+1>=self.scrollWidth and not self.connected:
                # print("denny chinito is here")
                self.horizontalScrollBar.sliderMoved['int'].connect(self.slideVal)
                self.connected=True
            elif self.ind>self.scrollWidth and self.connected:
                # print("deenah latina is here")
                # print(100 * self.scrollWidth / (self.ind - self.scrollWidth))
                self.horizontalScrollBar.setPageStep(100 * self.scrollWidth / (self.ind - self.scrollWidth))
            # print("deenah latina is gone")
            self.ind+=1
    def writeSQL(self):
        t_zero = timestampd.value
        song = songdump
        event_time = lickdump[:]
        #####################
        sevent_time='['
        for i,eventee in enumerate(event_time):
            sevent_time+=(('%.4f' % event_time[i])+',')
        sevent_time=sevent_time[:-1]+']'
        #######formatting storage string
        # print(sevent_time)
        direction = dump[0]
        correct = dump[1]
        difficulty = dump[2]
        # print(self.session_ID, self.ind, str(t_zero), self.song_mem[0], str(event_time), difficulty, correct,direction)

        self.cursor.execute(
            "INSERT INTO  Temporal_Trails ( Session_ID, Trail_ID, SequenceStartTime, Song, LickTime, Difficulty, Correctness, LickResult) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (self.session_ID, self.ind, str(t_zero), self.song_mem[0], sevent_time, difficulty, correct,direction))
        self.cnx.commit()

    def writeCSV(self):
        t_zero = timestampd.value
        song = songdump
        event_time = lickdump[:]
        direction = dump[0]
        correct = dump[1]
        difficulty = dump[2]
        self.writer.writerow([self.session_ID, self.ind, str(t_zero), self.song_mem[0], str(event_time), difficulty, correct,direction])



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
        print('update_main')
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

        # print("bro watch outtttttttttt")
        # print(event_time)
        # print(dump[:])
        ########################### Update color bar graph

        # print(ind)

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
        self.ax3.set_xlim(0, 6)
        self.ax3.set_ylim(-1, 1)
        self.ax3.set_title('Most recent')
        self.ax3.set_yticks([-1, 0, 1])
        self.ax3.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax3.axhline(y=0, color='k')
        self.ax3.axvline(x=2,color='r')
        ### second guy
        self.ax4 = self.figure.add_subplot(312)
        self.ax4.set_xlim(0, 6)
        self.ax4.set_ylim(-1, 1)
        self.ax4.set_title('Last Trail')
        self.ax4.set_yticks([-1, 0, 1])
        self.ax4.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax4.axhline(y=0, color='k')
        self.ax4.axvline(x=2, color='r')
        ### third guy
        self.ax5 = self.figure.add_subplot(313)
        self.ax5.set_xlim(0, 6)
        self.ax5.set_ylim(-1, 1)
        self.ax5.set_title('2 Trails Ago')
        self.ax5.set_yticks([-1, 0, 1])
        self.ax5.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax5.axhline(y=0, color='k')
        self.ax5.axvline(x=2, color='r')
        self.figure.subplots_adjust(hspace=.75)

        temp = patches.Rectangle(
            (1, 1),  # (x,y)
            .01,  # width
            1,  # height
        )

        self.del_but1 = []
        self.del_but2 = []
        self.del_but3 = []
        self.del_but1.append(self.ax3.add_patch(copy.copy(temp)))
        self.del_but2.append(self.ax4.add_patch(copy.copy(temp)))
        self.del_but3.append(self.ax4.add_patch(copy.copy(temp)))

        self.bar_cache = []
    def update_figure(self,ind):
        print('update_side')
        event_time = lickdump[:]
        # print(event_time)
        ld = lickdirection[:]
       # print(ind)
       #  print("bro watch innnnnnnnnnn")
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
        tempy = []
        a_tempy = []
        for eventee, l in zip(event_time, ld):
            tempy.append(patches.Rectangle(
                (eventee, -1 if l == 0 else 0),  # (x,y)
                .05,  # width
                1,  # height
            ))
        #    print(temp.get_axes())
        # print("made it to 2")
        for term in tempy: a_tempy.append(copy.copy(term))
        self.bar_cache.insert(0, a_tempy)  # load up history list
        if len(self.bar_cache) == 4:
            self.bar_cache.pop()
            #   print(bar_cache[0].get_axes())
        self.del_but1 = []
        for term in a_tempy:
            self.del_but1.append(self.ax3.add_patch(term))  # return delete button
        self.draw()
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
        self.draw()
        try:
            inst1 = []
            self.del_but2 = []
            for term in self.bar_cache[1]:
                inst1.append(copy.copy(term))
                # print(inst1[::-1][0].get_axes())
                self.del_but2.append(self.ax4.add_patch(inst1[::-1][0]))
                # print(inst1[::-1][0].get_axes())
            # print("made it to 4.3")
            self.ax4.set_title('Last Trail #%d' % (ind - 1))
        except IndexError:
            print("312 exception")
            pass;
        # print("made it to 5")
        self.draw()
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
        self.draw()
        #print(self.bar_cache)
        try:
            inst2 = []
            self.del_but3 = []
            for term in self.bar_cache[2]:
                inst2.append(copy.copy(term))
                self.del_but3.append(self.ax5.add_patch(inst2[::-1][0]))

            self.ax5.set_title('2 Trails Ago #%d' % (ind - 2))
            # print("made it to 5.3")
        except IndexError:
            print("313 exception")
            pass
        self.draw()
        #print("made it to 6")


                #self.draw()

def exitApp():
    slave.terminate()
    prep.ComPort.close()
    cursor = prep.cnx.cursor()
    cursor.execute(
            "INSERT INTO  Temporal_Session (Complete) VALUES (%s)",
            (1))
    prep.cnx.commit()
    prep.cnx.disconnect()
    prep.theFile.close()
    newName=prep.pathName[:-4]+str(ex.session_ID)+'.csv'
    os.rename(prep.pathName,newName)
    print('leaving with hella style')
        # ...
        # os.rename(filename, filename[7:])
    sys.exit()
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    prep = Luncher()
    app.exec_()

    print(prep.ComPort)
    print(prep.theFile)
    print(prep.cnx)
    momom=5
    ind = 1
    l_diff = [0, ]
    event_time = []

    #`Animal_ID`, `Training`, `Punishment_Duration`, `Tone_Duration`, `Ttime_Between_Tones`, `Lickwindow_Duration`, `R_Opentime`, `L_Opentime`, `Trial_Limit`, `min_Difficulty`, `max_Difficulty`, `Drip_Delay`    #
    config=[1       ,1          ,1.5                    ,2.5            ,0.5                    ,.25                ,.65            ,.65            ,200        ,4              ,20                 , 5]
    dbName='Salk'

    try:
        prep.ComPort.close()
        new_stuff = Value('b', False)
        dump = Array('i', range(3))
        timestampd = Value('f', 0.0)
        songdump = Array('i', range(4))
        # l = Array('f',100)
        manager = Manager()
        lickdump = manager.list()
        lickdirection = manager.list()
        time.sleep(2)
        slave = Process(target=Serial_Process, args=(prep.portName,lickdirection, dump, lickdump, songdump, timestampd, new_stuff))
        slave.start()
        mainApp = QApplication(sys.argv)
        ex = App(prep.cnx)
        mainApp.exec_()
    except Exception:
        pass
    exitApp()

