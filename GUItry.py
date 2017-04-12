import sys
from PyQt5 import QtCore, QtWidgets, QtGui,QtMultimedia
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
import os, datetime
from luncher import Luncher
from settings import Settings
import camera
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
        self.flowButtonStatus = True
        ###########Obtain Session ID from Server
        #TODO: Insert actual settings
        config=prep.settingsWidget.jsettings


        self.cursor.execute(
            "INSERT INTO  Temporal_Session (Animal_ID, Training, Punishment_Duration, Tone_Duration, Ttime_Between_Tones, Lickwindow_Duration, R_Opentime, L_Opentime, Trial_Limit, min_Difficulty, max_Difficulty, Drip_Delay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (config['session_default']['animal_id'], config['mcu_config']['training_phase'], config['mcu_config'][
                'punishment_duration'], config['mcu_config']['tone_duration'], config['mcu_config'][
                'time_between_tones'], config['mcu_config']['lickwindow_duration'], config['mcu_config'][
                'valve_open_time'], config['mcu_config']['valve_open_time'], config['mcu_config']['trial_number'], config['mcu_config']['min_difficulty'],
             config['mcu_config']['max_difficulty'], config['mcu_config']['drip_delay_time']))
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
        self.Cam=camera.Camera()


        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(200)

        self.ind = 1
        self.totalTarget=0
        self.totalCorrect=0
        self.totalNo=0
        self.totalWrong=0
        self.itargetCorrect=0
        self.itargetWrong=0
        self.intargetCorrect = 0
        self.intargetWrong = 0


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
        # self.pauseButton.setIcon(QtGui.QIcon('pause.png'))
        # self.pauseButton.setIconSize(QtCore.QSize(75, 75))
        self.statusbar.showMessage(prep.pathName)

        self.startButton.clicked.connect(self.flowControl)
        self.actionSettings.triggered.connect(self.openSettings)

        cameraDevice = ''

        videoDevicesGroup = QtWidgets.QActionGroup(self)
        videoDevicesGroup.setExclusive(True)

        for deviceName in QtMultimedia.QCamera.availableDevices():
            description = QtMultimedia.QCamera.deviceDescription(deviceName)
            videoDeviceAction = QtWidgets.QAction(description, videoDevicesGroup)
            videoDeviceAction.setCheckable(True)
            videoDeviceAction.setData(deviceName)

            if not cameraDevice:
                cameraDevice = deviceName
                videoDeviceAction.setChecked(True)
            print(videoDeviceAction)
            self.menuCameras.addAction(videoDeviceAction)

        videoDevicesGroup.triggered.connect(self.Cam.updateCameraDevice)
        self.menubar.addAction(self.menuCameras.menuAction())

        self.show()


        # time.sleep(3)
        # self.update_figure()
        #
        # time.sleep(3)
        # self.update_figure()
        # time.sleep(3)
        # self.update_figure()

    def updateCameraDevice(self, action):
        self.setCamera(action.data())

    def flowControl(self):
        if self.flowButtonStatus:
            try:
                self.toggleFlow(False)
                self.startButton.setIcon(QtGui.QIcon('pause.png'))
                self.flowButtonStatus = not self.flowButtonStatus
                self.flushButton.setEnabled(False)
            except Exception as e:
                print(str(e))

        else:
            try:
                self.toggleFlow(True)
                self.startButton.setIcon(QtGui.QIcon('play.png'))
                self.flowButtonStatus = not self.flowButtonStatus
                self.flushButton.setEnabled(True)
            except Exception as e:
                print(str(e))
    def toggleFlow(self,start_stop):
        start_pause.value=start_stop
        print(send_pending.value)
        send_pending.value=1
        print(send_pending.value)
        print('ran def toggle flow')

    def toggleFlush(self,start_stop):
        flush_stop.value = start_stop
        print(send_pending.value)
        send_pending.value = 2
        print(send_pending.value)
        print('ran def toggle flow')

    def openSettings(self):

        #send pause signal
        #wait for confirmed pause
        print("brother 111111111")
        self.settingsWindow = Settings("COM4")
        print("brother 222222222")

        self.settingsWindow.downloadButton.clicked.connect(self.download_settings)

        print("brother 333333333")

    def download_settings(self):
        print("attempt to download settings")
        try:
            settings_dump[:]=[]
        except Exception as e:
            print(str(e))
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
       # MainWindow.resize(1146, 650)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 603, 545))
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
        # self.Cam = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Cam.sizePolicy().hasHeightForWidth())
        self.Cam.setSizePolicy(sizePolicy)
        self.Cam.setMinimumSize(QtCore.QSize(50, 0))
        self.Cam.setMaximumSize(QtCore.QSize(400, 16777215))
        self.Cam.setObjectName("Cam")
        self.gridLayout.addWidget(self.Cam, 0, 7, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_4.addWidget(self.line_6)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.trailText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trailText.sizePolicy().hasHeightForWidth())
        self.trailText.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trailText.setFont(font)
        self.trailText.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.trailText.setObjectName("trailText")
        self.verticalLayout_4.addWidget(self.trailText)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.targetText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetText.sizePolicy().hasHeightForWidth())
        self.targetText.setSizePolicy(sizePolicy)
        self.targetText.setMinimumSize(QtCore.QSize(0, 40))
        self.targetText.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.targetText.setFont(font)
        self.targetText.setAlignment(QtCore.Qt.AlignCenter)
        self.targetText.setObjectName("targetText")
        self.gridLayout_5.addWidget(self.targetText, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 40))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_5.addWidget(self.line_10, 2, 1, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_5.addWidget(self.line_8, 0, 1, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_14.setObjectName("label_14")
        self.gridLayout_6.addWidget(self.label_14, 0, 0, 1, 1)
        self.targetCorrect = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetCorrect.sizePolicy().hasHeightForWidth())
        self.targetCorrect.setSizePolicy(sizePolicy)
        self.targetCorrect.setMinimumSize(QtCore.QSize(50, 0))
        self.targetCorrect.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.targetCorrect.setFont(font)
        self.targetCorrect.setObjectName("targetCorrect")
        self.gridLayout_6.addWidget(self.targetCorrect, 1, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_16.setObjectName("label_16")
        self.gridLayout_6.addWidget(self.label_16, 0, 2, 1, 1)
        self.targetWrong = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetWrong.sizePolicy().hasHeightForWidth())
        self.targetWrong.setSizePolicy(sizePolicy)
        self.targetWrong.setMinimumSize(QtCore.QSize(50, 0))
        self.targetWrong.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.targetWrong.setFont(font)
        self.targetWrong.setObjectName("targetWrong")
        self.gridLayout_6.addWidget(self.targetWrong, 1, 2, 1, 1)
        self.line_14 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_14.sizePolicy().hasHeightForWidth())
        self.line_14.setSizePolicy(sizePolicy)
        self.line_14.setMaximumSize(QtCore.QSize(16777215, 25))
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.gridLayout_6.addWidget(self.line_14, 0, 1, 1, 1)
        self.line_16 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_16.sizePolicy().hasHeightForWidth())
        self.line_16.setSizePolicy(sizePolicy)
        self.line_16.setMaximumSize(QtCore.QSize(16777215, 50))
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.gridLayout_6.addWidget(self.line_16, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_6, 2, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_18.setObjectName("label_18")
        self.gridLayout_7.addWidget(self.label_18, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_19.setObjectName("label_19")
        self.gridLayout_7.addWidget(self.label_19, 0, 2, 1, 1)
        self.ntargetCorrect = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ntargetCorrect.sizePolicy().hasHeightForWidth())
        self.ntargetCorrect.setSizePolicy(sizePolicy)
        self.ntargetCorrect.setMinimumSize(QtCore.QSize(50, 0))
        self.ntargetCorrect.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ntargetCorrect.setFont(font)
        self.ntargetCorrect.setObjectName("ntargetCorrect")
        self.gridLayout_7.addWidget(self.ntargetCorrect, 1, 0, 1, 1)
        self.ntargetWrong = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ntargetWrong.sizePolicy().hasHeightForWidth())
        self.ntargetWrong.setSizePolicy(sizePolicy)
        self.ntargetWrong.setMinimumSize(QtCore.QSize(50, 0))
        self.ntargetWrong.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ntargetWrong.setFont(font)
        self.ntargetWrong.setObjectName("ntargetWrong")
        self.gridLayout_7.addWidget(self.ntargetWrong, 1, 2, 1, 1)
        self.line_15 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_15.sizePolicy().hasHeightForWidth())
        self.line_15.setSizePolicy(sizePolicy)
        self.line_15.setMaximumSize(QtCore.QSize(16777215, 25))
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.gridLayout_7.addWidget(self.line_15, 0, 1, 1, 1)
        self.line_17 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_17.sizePolicy().hasHeightForWidth())
        self.line_17.setSizePolicy(sizePolicy)
        self.line_17.setMaximumSize(QtCore.QSize(16777215, 50))
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.gridLayout_7.addWidget(self.line_17, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_7, 2, 2, 1, 1)
        self.ntargetText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ntargetText.sizePolicy().hasHeightForWidth())
        self.ntargetText.setSizePolicy(sizePolicy)
        self.ntargetText.setMinimumSize(QtCore.QSize(0, 40))
        self.ntargetText.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ntargetText.setFont(font)
        self.ntargetText.setAlignment(QtCore.Qt.AlignCenter)
        self.ntargetText.setObjectName("ntargetText")
        self.gridLayout_5.addWidget(self.ntargetText, 1, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(0, 40))
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 0, 2, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_5.addWidget(self.line_9, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_5)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_4.addWidget(self.line_7)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)
        self.correctText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.correctText.sizePolicy().hasHeightForWidth())
        self.correctText.setSizePolicy(sizePolicy)
        self.correctText.setMinimumSize(QtCore.QSize(0, 30))
        self.correctText.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.correctText.setFont(font)
        self.correctText.setAlignment(QtCore.Qt.AlignCenter)
        self.correctText.setObjectName("correctText")
        self.gridLayout_3.addWidget(self.correctText, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.wrongText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wrongText.sizePolicy().hasHeightForWidth())
        self.wrongText.setSizePolicy(sizePolicy)
        self.wrongText.setMinimumSize(QtCore.QSize(0, 30))
        self.wrongText.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.wrongText.setFont(font)
        self.wrongText.setAlignment(QtCore.Qt.AlignCenter)
        self.wrongText.setObjectName("wrongText")
        self.gridLayout_3.addWidget(self.wrongText, 1, 2, 1, 1)
        self.noText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noText.sizePolicy().hasHeightForWidth())
        self.noText.setSizePolicy(sizePolicy)
        self.noText.setMinimumSize(QtCore.QSize(0, 30))
        self.noText.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.noText.setFont(font)
        self.noText.setAlignment(QtCore.Qt.AlignCenter)
        self.noText.setObjectName("noText")
        self.gridLayout_3.addWidget(self.noText, 1, 4, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.gridLayout_3.addWidget(self.line_12, 0, 1, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.centralwidget)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.gridLayout_3.addWidget(self.line_13, 1, 3, 1, 1)
        self.line_18 = QtWidgets.QFrame(self.centralwidget)
        self.line_18.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.gridLayout_3.addWidget(self.line_18, 1, 1, 1, 1)
        self.line_19 = QtWidgets.QFrame(self.centralwidget)
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.gridLayout_3.addWidget(self.line_19, 0, 3, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 9, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout.addWidget(self.line_11, 0, 6, 1, 1)
        self.line_20 = QtWidgets.QFrame(self.centralwidget)
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.gridLayout.addWidget(self.line_20, 0, 8, 1, 1)
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
        self.startButton.setText("")
        self.startButton.setObjectName("startButton")
        self.verticalLayout_3.addWidget(self.startButton)
        self.flushButton = QtWidgets.QToolButton(self.centralwidget)
        self.flushButton.setObjectName("flushButton")
        self.verticalLayout_3.addWidget(self.flushButton)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 2, 3, 1, 1)
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setObjectName("quitButton")
        self.gridLayout_2.addWidget(self.quitButton, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1146, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCameras = QtWidgets.QMenu(self.menubar)
        self.menuCameras.setObjectName("menuCameras")
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
        self.menubar.addAction(self.menuCameras.menuAction())

        self.retranslateUi(MainWindow)
        self.horizontalScrollBar.sliderMoved['int'].connect(self.horizontalScrollBar.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.song1.setText(_translate("MainWindow", "N/A"))
        self.song2.setText(_translate("MainWindow", "N/A"))
        self.song3.setText(_translate("MainWindow", "N/A"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Stats</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "Total Trails:"))
        self.trailText.setText(_translate("MainWindow", "trailText"))
        self.targetText.setText(_translate("MainWindow", "targetText"))
        self.label_10.setText(_translate("MainWindow", "Target Trails"))
        self.label_14.setText(_translate("MainWindow",
                                         "<html><head/><body><p><span style=\" font-family:\'Verdana,Arial,Tahoma,Calibri,Geneva,sans-serif\'; font-size:13px; color:#00ff00; background-color:#fafafa;\">√</span></p></body></html>"))
        self.targetCorrect.setText(_translate("MainWindow", "TextLabel"))
        self.label_16.setText(_translate("MainWindow",
                                         "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">X</span></p></body></html>"))
        self.targetWrong.setText(_translate("MainWindow", "TextLabel"))
        self.label_18.setText(_translate("MainWindow",
                                         "<html><head/><body><p><span style=\" font-family:\'Verdana,Arial,Tahoma,Calibri,Geneva,sans-serif\'; font-size:13px; color:#00ff00; background-color:#fafafa;\">√</span></p></body></html>"))
        self.label_19.setText(_translate("MainWindow",
                                         "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">X</span></p></body></html>"))
        self.ntargetCorrect.setText(_translate("MainWindow", "TextLabel"))
        self.ntargetWrong.setText(_translate("MainWindow", "TextLabel"))
        self.ntargetText.setText(_translate("MainWindow", "ntargetText"))
        self.label_12.setText(_translate("MainWindow", "Non-Target"))
        self.label_3.setText(_translate("MainWindow", "$ Wrong"))
        self.correctText.setText(_translate("MainWindow", "correctText"))
        self.label_9.setText(_translate("MainWindow", "% Nolick"))
        self.label_2.setText(_translate("MainWindow", "% Correct"))
        self.wrongText.setText(_translate("MainWindow", "wrongText"))
        self.noText.setText(_translate("MainWindow", "noText"))
        self.sessionID.setText(_translate("MainWindow", "Session :1"))
        self.port_Status.setText(_translate("MainWindow", "Port:"))
        self.db_status.setText(_translate("MainWindow", "SQL(connected):"))
        self.timeText.setText(_translate("MainWindow", "TIME"))
        #self.startButton.setText(_translate("MainWindow", "Start"))
        self.flushButton.setText(_translate("MainWindow", "Flush"))
        self.quitButton.setText(_translate("MainWindow", "Quit n Save"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCameras.setTitle(_translate("MainWindow", "Cameras"))
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
            self.toggleFlush(True)
            self.flushButton.setIcon(QtGui.QIcon('flushOn.png'))
            self.flushButton.setText('Stop Flush')

        else:
            self.toggleFlush(False)
            self.flushButton.setIcon(QtGui.QIcon('flushOff.png'))
            self.flushButton.setText('Flush')
        self.flushButtonStatus= not self.flushButtonStatus

    def update_figure(self):
        if self.ind==1:
            self.startTime = datetime.datetime.now().replace(microsecond=0)
        SONGDICT={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G'}
        song_alpha=[]
        if not new_stuff.value:
            try:
                self.timeText.setText('T+ '+str(datetime.datetime.now().replace(microsecond=0)- self.startTime))
            except Exception as e:
                print('this is bad'+str(e))
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


            self.totalTarget += 1 if self.mainPlot.difficulty == 0 else 0
            self.totalCorrect += 1 if self.mainPlot.correct == 0 and self.mainPlot.direction != 0 else 0
            self.totalNo += 1 if self.mainPlot.direction == 0 else 0
            self.totalWrong += 1 if self.mainPlot.correct == 1 and self.mainPlot.direction != 0 else 0
            self.itargetCorrect += 1 if self.mainPlot.difficulty == 0 and self.mainPlot.correct == 0 and self.mainPlot.direction != 0 else 0
            self.itargetWrong += 1 if self.mainPlot.difficulty == 0 and self.mainPlot.correct == 1 and self.mainPlot.direction != 0 else 0
            self.intargetCorrect += 1 if self.mainPlot.difficulty != 0 and self.mainPlot.correct == 0 and self.mainPlot.direction != 0 else 0
            self.intargetWrong += 1 if self.mainPlot.difficulty != 0 and self.mainPlot.correct == 1 and self.mainPlot.direction != 0 else 0
            chinita=0
            try:
                #TODO: insert total stats at the end of session
                self.targetText.setText(str(self.totalTarget))
                self.ntargetText.setText(str(self.ind - self.totalTarget))
                self.trailText.setText(str(self.ind))

                try:
                    print('aaaaaaaaaaaaaa', self.itargetCorrect)
                    self.targetCorrect.setText("{0:.2f}".format(self.itargetCorrect/self.totalTarget*100)+'%')

                except Exception as e:
                    print(str(e))
                    self.targetCorrect.setText('0 %')
                try:
                    print(self.itargetWrong)
                    self.targetWrong.setText("{0:.2f}".format(self.itargetWrong/ self.totalTarget*100)+'%')

                except Exception as e:
                    print(str(e))
                    self.targetWrong.setText('0 %')
                try:
                    print(self.intargetCorrect)
                    self.ntargetCorrect.setText("{0:.2f}".format(self.intargetCorrect / (self.ind - self.totalTarget) * 100)+'%')

                except Exception as e:
                    print(str(e))
                    self.ntargetCorrect.setText('0 %')
                try:
                    print(self.intargetCorrect)
                    self.ntargetWrong.setText("{0:.2f}".format(self.intargetWrong / (self.ind - self.totalTarget) * 100)+'%')

                except Exception as e:
                    print(str(e))
                    self.ntargetWrong.setText('0 %')

                self.correctText.setText("{0:.2f}".format(self.totalCorrect/self.ind*100))
                chinita += 1
                self.wrongText.setText("{0:.2f}".format(self.totalWrong/self.ind*100))
                chinita += 1
                self.noText.setText("{0:.2f}".format(self.totalNo/self.ind*100))
                chinita += 1

            except Exception as e:
                print(str(e),'  ',chinita)

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
        self.ax2.set_ylim(0, 50)
        self.del_but0 = self.ax2.step(1, 1)


    def update_figure(self,ind):
        print('update_main')
        self.ind=ind
        # idump = [self.direction, self.correct, self.difficulty]
        # lickdump = event_time
        # songdump = song
        # timestampd = t_zero
        t_zero = timestampd.value

        event_time = lickdump[:]
        self.direction = dump[0]
        self.correct = dump[1]
        self.difficulty = dump[2]

        # print("bro watch outtttttttttt")
        # print(event_time)
        # print(dump[:])
        ########################### Update color bar graph

        # print(ind)

        # result[1]
        fill = "red" if self.correct else "green"
        # print(fill)
        # print("made it to 1")
        self.ax1.add_patch(
            patches.Rectangle(
                (ind - 1, -1 if self.direction == -1 else 0),  # (x,y)
                1,  # width
                0.01 if self.direction == 0 else 1,  # height
                facecolor=fill,
            )
        )
        #  print("made it to 2")


        #  print("made it to 3")
        ###################### Update self.difficulty graph
        l_diff.append(self.difficulty)
        now = time.time()
        #  print("made it to 4")
        # print(list(range(ind+1)), self.difficulty)
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
        self.ax3.axvline(x=1.85,color='r')
        ### second guy
        self.ax4 = self.figure.add_subplot(312)
        self.ax4.set_xlim(0, 6)
        self.ax4.set_ylim(-1, 1)
        self.ax4.set_title('Last Trail')
        self.ax4.set_yticks([-1, 0, 1])
        self.ax4.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax4.axhline(y=0, color='k')
        self.ax4.axvline(x=1.85, color='r')
        ### third guy
        self.ax5 = self.figure.add_subplot(313)
        self.ax5.set_xlim(0, 6)
        self.ax5.set_ylim(-1, 1)
        self.ax5.set_title('2 Trails Ago')
        self.ax5.set_yticks([-1, 0, 1])
        self.ax5.set_yticklabels(['Left', 'No lick', 'Right'])
        self.ax5.axhline(y=0, color='k')
        self.ax5.axvline(x=1.85, color='r')
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
    cursor.execute("update  Temporal_Session set Complete=%s where id = %s",(1,ex.session_ID))
    prep.cnx.commit()
    prep.cnx.disconnect()
    prep.theFile.close()
    newName=prep.pathName[:-4]+str(ex.session_ID)+'.csv'
    os.chdir(prep.defaultPath)
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
        send_pending = Value('i', 0)# 0 is nothing, 1 is start/pause download, 2 is flush/stop flush,3 is settings download
        start_pause = Value('b', False)
        flush_stop = Value('b', False)
        settings_dump = Array('i', range(4))
        # l = Array('f',100)
        manager = Manager()
        lickdump = manager.list()
        lickdirection = manager.list()
        time.sleep(2)
        slave = Process(target=Serial_Process, args=(prep.portName,lickdirection, dump, lickdump, songdump, timestampd, new_stuff, send_pending,start_pause,settings_dump,flush_stop))
        slave.start()
        mainApp = QApplication(sys.argv)
        ex = App(prep.cnx)
        mainApp.exec_()
    except Exception as e:
        print("realy bad stuff happend, quitting",str(e))
        pass
    exitApp()

