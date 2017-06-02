# -*- coding: utf-8 -*-
from serial.tools import list_ports
import fnmatch
import serial
import mysql.connector
import time,sys,json
import csv
from settings import Settings
from fakeSQL import *
# Form implementation generated from reading ui file 'luncherUI.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Luncher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settingsWidget = Settings(self,mode=2)
        self.setupUi(self)

        self.scannerDrop.addItem("Select...")

        ports = list(list_ports.comports())
        for p in ports:
            self.serialDrop.addItem(str(p))
            if "USB Serial Device" in str(p):
                self.scannerDrop.addItem(str(p))

        self.scannerDrop.currentIndexChanged.connect(self.linkScanner)
        self.serialButton.clicked.connect(self.openSerial)
        self.sqlButton.clicked.connect(self.openSQL)
        self.checkButton.clicked.connect(self.checkIn)
        self.lunchButton.setEnabled(False)
        self.lunchButton.clicked.connect(self.gtfo)
        self.lunchButton.setAutoDefault(True)

        self.userText.setText(self.settingsWidget.jsettings['session_default']['db_login'])
        self.passText.setText(self.settingsWidget.jsettings['session_default']['db_pass'])
        self.dbText.setText(self.settingsWidget.jsettings['session_default']['db_schema'])
        self.ipText.setText(self.settingsWidget.jsettings['session_default']['db_url'])
        self.defaultPath=self.settingsWidget.jsettings['session_default']['path']
        self.mouseBox.setText(str(self.settingsWidget.jsettings['session_default']['animal_id']))
        self.cageBox.setText(str(self.settingsWidget.jsettings['session_default']['cage_id']))

        self.show()
        self.broImReady=[0,0,0]


    def gtfo(self):
        
        self.settingsWidget.ComPort=self.portName

        with open('settings.json', 'w') as outfile:
            json.dump(self.settingsWidget.jsettings, outfile)
        try:
            thepoop=self.settingsWidget.download()
            print(str(thepoop)+"mclaunchface")
            self.ComPort.write(thepoop)
            self.close()
            print("just pooped everywhere")
        except Exception as e:
            print('Download Failure: '+ str(e))

            
        self.settingsWidget.jsettings['session_default']['db_login']    =self.userText.text()
        self.settingsWidget.jsettings['session_default']['db_pass']     =self.passText.text()
        self.settingsWidget.jsettings['session_default']['db_schema']   =self.dbText.text()
        self.settingsWidget.jsettings['session_default']['db_url']      =self.ipText.text()
        self.settingsWidget.jsettings['session_default']['path'] = self.defaultPath
        self.mouse_ID=int(self.mouseBox.text())
        self.cage_ID=int(self.cageBox.text())
        self.settingsWidget.jsettings['session_default']['animal_id'] = self.mouse_ID
        self.settingsWidget.jsettings['session_default']['cage_id'] = self.cage_ID

        self.settingsWidget.jsettings['mcu_config']['song1'] = self.settingsWidget.song1.text()
        self.settingsWidget.jsettings['mcu_config']['song2'] = self.settingsWidget.song2.text()
        self.settingsWidget.jsettings['mcu_config']['song3'] = self.settingsWidget.song3.text()
        self.settingsWidget.jsettings['mcu_config']['song4'] = self.settingsWidget.song4.text()

        self.settingsWidget.jsettings['mcu_config']['encourage'] = self.settingsWidget.encourageBox.value()
        self.settingsWidget.jsettings['mcu_config']['encourage_delay'] = self.settingsWidget.encourageDelayBox.value()

        self.settingsWidget.jsettings['mcu_config']['drip_delay_time'] = self.settingsWidget.dripBox.value()
        self.settingsWidget.jsettings['mcu_config']['punishment_duration'] = self.settingsWidget.punishBox.value()
        self.settingsWidget.jsettings['mcu_config']['delay_duration'] = self.settingsWidget.delayBox.value()
        self.settingsWidget.jsettings['mcu_config']['tone_duration'] = self.settingsWidget.toneBox.value()
        self.settingsWidget.jsettings['mcu_config']['time_between_tones'] = self.settingsWidget.betweenToneBox.value()
        self.settingsWidget.jsettings['mcu_config']['valve_open_time_L'] = self.settingsWidget.valveBoxL.value()
        self.settingsWidget.jsettings['mcu_config']['valve_open_time_R'] = self.settingsWidget.valveBoxR.value()
        self.settingsWidget.jsettings['mcu_config']['lickwindow_duration'] = self.settingsWidget.lickBox.value()
        self.settingsWidget.jsettings['mcu_config']['trial_number'] = self.settingsWidget.trailBox.value()
        self.settingsWidget.jsettings['mcu_config']['min_difficulty'] = self.settingsWidget.minBox.value()
        self.settingsWidget.jsettings['mcu_config']['max_difficulty'] = self.settingsWidget.maxBox.value()
        self.settingsWidget.jsettings['mcu_config']['training_phase'] = 1 if self.settingsWidget.p1Button.isChecked() and self.settingsWidget.p2Button.isChecked() else 2
        self.settingsWidget.jsettings['session_default']['position'] += 1
        if self.settingsWidget.jsettings['session_default']['position'] == 5:
            self.settingsWidget.jsettings['session_default']['position'] = 1



        self.close()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1137, 801)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_2.addWidget(self.line_5, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 15, 0, 1, 1)
        self.stepThree = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stepThree.setFont(font)
        self.stepThree.setObjectName("stepThree")
        self.gridLayout.addWidget(self.stepThree, 16, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.serialDrop = QtWidgets.QComboBox(Form)
        self.serialDrop.setObjectName("serialDrop")
        self.horizontalLayout.addWidget(self.serialDrop)
        self.serialButton = QtWidgets.QPushButton(Form)
        self.serialButton.setObjectName("serialButton")
        self.horizontalLayout.addWidget(self.serialButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.userText = QtWidgets.QLineEdit(Form)
        self.userText.setObjectName("userText")
        self.horizontalLayout_5.addWidget(self.userText)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.passText = QtWidgets.QLineEdit(Form)
        self.passText.setObjectName("passText")
        self.horizontalLayout_5.addWidget(self.passText)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.dbText = QtWidgets.QLineEdit(Form)
        self.dbText.setObjectName("dbText")
        self.horizontalLayout_5.addWidget(self.dbText)
        self.gridLayout.addLayout(self.horizontalLayout_5, 7, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.ipText = QtWidgets.QLineEdit(Form)
        self.ipText.setObjectName("ipText")
        self.horizontalLayout_4.addWidget(self.ipText)
        self.sqlButton = QtWidgets.QPushButton(Form)
        self.sqlButton.setObjectName("sqlButton")
        self.horizontalLayout_4.addWidget(self.sqlButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 12, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.initialWeight = QtWidgets.QDoubleSpinBox(Form)
        self.initialWeight.setObjectName("initialWeight")
        self.horizontalLayout_3.addWidget(self.initialWeight)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.line_9 = QtWidgets.QFrame(Form)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_3.addWidget(self.line_9)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.currentWeight = QtWidgets.QDoubleSpinBox(Form)
        self.currentWeight.setObjectName("currentWeight")
        self.horizontalLayout_3.addWidget(self.currentWeight)
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.gridLayout.addLayout(self.horizontalLayout_3, 17, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.stepTwo = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stepTwo.setFont(font)
        self.stepTwo.setObjectName("stepTwo")
        self.gridLayout.addWidget(self.stepTwo, 5, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_15.addWidget(self.label_21)
        self.cageBox = QtWidgets.QLineEdit(Form)
        self.cageBox.setMinimumSize(QtCore.QSize(60, 0))
        self.cageBox.setObjectName("cageBox")
        self.horizontalLayout_15.addWidget(self.cageBox)
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_15.addWidget(self.label_22)
        self.mouseBox = QtWidgets.QLineEdit(Form)
        self.mouseBox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.mouseBox.setObjectName("mouseBox")
        self.horizontalLayout_15.addWidget(self.mouseBox)
        self.checkButton = QtWidgets.QPushButton(Form)
        self.checkButton.setObjectName("checkButton")
        self.horizontalLayout_15.addWidget(self.checkButton)
        self.line_8 = QtWidgets.QFrame(Form)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout_15.addWidget(self.line_8)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_15.addWidget(self.label_2)
        self.scannerDrop = QtWidgets.QComboBox(Form)
        self.scannerDrop.setMinimumSize(QtCore.QSize(100, 0))
        self.scannerDrop.setObjectName("scannerDrop")
        self.horizontalLayout_15.addWidget(self.scannerDrop)
        self.gridLayout.addLayout(self.horizontalLayout_15, 13, 0, 1, 1)
        self.stepOne = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stepOne.setFont(font)
        self.stepOne.setObjectName("stepOne")
        self.gridLayout.addWidget(self.stepOne, 0, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 19, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 18, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(Form)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 8, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.lunchButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lunchButton.sizePolicy().hasHeightForWidth())
        self.lunchButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(16)
        self.lunchButton.setFont(font)
        self.lunchButton.setAutoDefault(True)
        self.lunchButton.setDefault(False)
        self.lunchButton.setObjectName("lunchButton")
        self.gridLayout_2.addWidget(self.lunchButton, 0, 4, 1, 1)
#        self.settingsWidget = QtWidgets.QWidget(Form)
        self.settingsWidget.setObjectName("settingsWidget")
        self.gridLayout_2.addWidget(self.settingsWidget, 0, 2, 1, 1)
        self.line_6 = QtWidgets.QFrame(Form)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_2.addWidget(self.line_6, 0, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Behavior Luncher"))
        self.stepThree.setText(_translate("Form", "Step 4: Record Weight"))
        self.serialButton.setText(_translate("Form", "Connect"))
        self.label_6.setText(_translate("Form", "User"))
        self.userText.setText(_translate("Form", "dennis"))
        self.label_7.setText(_translate("Form", "Pass"))
        self.passText.setText(_translate("Form", "rh960615"))
        self.label_8.setText(_translate("Form", "Database"))
        self.dbText.setText(_translate("Form", "Salk"))
        self.label_5.setText(_translate("Form", "ServerAddress"))
        self.ipText.setText(_translate("Form", "ssh.dennisren.com"))
        self.sqlButton.setText(_translate("Form", "Connect"))
        self.label.setText(_translate("Form", "Step 3: Who\'s There?"))
        self.label_3.setText(_translate("Form", "Initial Weight"))
        self.label_9.setText(_translate("Form", "Grams"))
        self.label_10.setText(_translate("Form", "Current Weight"))
        self.label_11.setText(_translate("Form", "Grams"))
        self.label_4.setText(_translate("Form", "Choose one or both below (2 alone, 3 alone, or 2 and 3)"))
        self.stepTwo.setText(_translate("Form", "Step 2: Connect to Database"))
        self.label_21.setText(_translate("Form", "Cage ID"))
        self.label_22.setText(_translate("Form", "Mouse ID"))
        self.checkButton.setText(_translate("Form", "Check-In"))
        self.label_2.setText(_translate("Form", "Scanner:"))
        self.stepOne.setText(_translate("Form", "Step 1: Connect to Serial"))
        self.lunchButton.setText(_translate("Form", "Launch"))


    def checkIn(self):
        print("attempting to checkin")
        query = ("SELECT SID,Nickname from animal_control "
                 "Where Cage_ID=%s and In_Cage_ID=%s")
        print("attempting to checkin 2")
        try:

            self.nickName = 'default'  # get first shit of tuple
            self.SID = 0
            self.cursor.execute(query, (int(self.cageBox.text()), int(self.mouseBox.text())))
            #########################################
            print("attempting to checkin 3")
            self.broImReady[2] = 1
            self.lunchButton.setEnabled(sum(self.broImReady) == 3)

            fetch=self.cursor.fetchone()
            self.nickName = fetch[1]  # get first shit of tuple
            self.SID= fetch[0]  # get first shit of tuple
            print("checkin success")

            self.label.setText('Step 4: Where there?   (Checked-in)')
        except Exception as e:
            print(str(e))
    def openSQL(self):

        server=self.ipText.text()
        user= self.userText.text()
        password= self.passText.text()
        database= self.dbText.text()
        # print(server,user,password,database)
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                      host=server,
                                      database=database)  # connect to Database
            self.sql_status='SQL connected'
            self.stepTwo.setText("Step 2: Connect to Database   (Connected)")
            self.broImReady[1] = 1
            if sum(self.broImReady) == 3:
                self.lunchButton.setEnabled(True)
        except Exception as e:
            self.sql_status = str(e)
            #now make face sql
            self.stepTwo.setText("Step 2: Connect to Database   (Failed)")
            self.cnx=fakeSQL()
            self.broImReady[1] = 1
            if sum(self.broImReady) == 3:
                self.lunchButton.setEnabled(True)
        self.textBrowser.append((self.sql_status))
        self.cursor=self.cnx.cursor()


    def linkScanner(self):
        print("it's lit fam")
        try:
            info = self.scannerDrop.currentText()
            filtered_wip = fnmatch.filter([info.split(' ', 1)[0]], 'COM?*')[0]

            self.scanPort = serial.Serial(filtered_wip)  # open the COM Port
            self.scanPort.baudrate = 9600  # set Baud rate
            self.scanPort.bytesize = 8  # Number of data bits = 8
            self.scanPort.parity = 'N'  # No parity
            self.scanPort.stopbits = 1  # Number of Stop bits = 1

            self.scantimer = QtCore.QTimer(self)
            self.scantimer.timeout.connect(self.read_ID)
            self.scantimer.start(200)
            self.textBrowser.append(str("scanner connected "+ filtered_wip))
        except Exception as e:
            self.textBrowser.append(str(e))

    def read_ID(self):

        index = 0
        out = []
        # print("hola amigo", self.scanPort.inWaiting())

        if self.scanPort.inWaiting() > 0:
            while self.scanPort.inWaiting() > 0:
                out.append(self.scanPort.read(1))
                index += 1

            # print(out)
            if len(out) <= 6:
                print (1, "reader detected, no (new) tag")  # return tuble, first err, sec load
            if out[0] != b'\x01':
                print (2, "no reader detected")
            if out[1] != b'\x09':
                print (3, "tag response error")

            ID_data = ''

            for i in reversed(range(len(out))):
                if int.from_bytes(out[i], byteorder='big') > 16:
                    ID_data = "%s%x" % (ID_data, int.from_bytes(out[i], byteorder='big'))
                else:
                    ID_data = "%s0%x" % (ID_data, int.from_bytes(out[i], byteorder='big'))
            CRC_ID = ID_data[8:12]
            Tag_ID = bytearray.fromhex(ID_data[2:18])
            rBCC = bytearray.fromhex(ID_data[0:2])
            cBCC = bytearray.fromhex(ID_data)
            BCC = 0
            for i in range(len(cBCC) - 2):
                BCC = BCC ^ cBCC[i + 1]
            if BCC != rBCC[0]:
                print (4, "BCC don't match")
            self.animalTag=ID_data[2:18]
            try:
                cursor = self.cnx.cursor()
                command=""" SELECT * FROM salk.animal_control Where salk.animal_control.Animal_ID="%s" ;"""% self.animalTag
                print(command)
                cursor.execute(command)
                self.bioInfo = cursor.fetchone()
                self.textBrowser.append(str(self.bioInfo)+"detected")
                self.mouseBox.setText(str(self.bioInfo[4]))
                self.cageBox.setText(str(self.bioInfo[3]))
                self.checkIn()
            except Exception as e:
                print(str(e))

    def openSerial(self):
        if self.serialButton.text()=='Connect':
            info=self.serialDrop.currentText()
            filtered_wip = fnmatch.filter([info.split(' ', 1)[0]], 'COM?*')[0]
            self.portName=filtered_wip
            # print(filtered_wip)
            try:
                self.ComPort = serial.Serial(filtered_wip)  # open the COM Port
                self.ComPort.baudrate = 19200  # set Baud rate
                self.ComPort.bytesize = 8  # Number of data bits = 8
                self.ComPort.parity = 'N'  # No parity
                self.ComPort.stopbits = 1  # Number of Stop bits = 1
                self.serial_status='connected'
                self.stepOne.setText('Step 1: Connect to Serial   (Connected)')
                self.broImReady[0] = 1
                self.serialButton.setText('Disconnect')
                self.textBrowser.append('Serial connected')
                self.lunchButton.setEnabled(sum(self.broImReady) == 3)
            except Exception as e:
                self.serial_status = str(e)
                self.textBrowser.append(self.serial_status)


        else:
            self.ComPort.close()
            self.serialButton.setText('Connect')
            self.broImReady[0] = 0
            self.textBrowser.append('Serial disconnected')
            self.lunchButton.setEnabled(sum(self.broImReady) == 3)
            self.stepOne.setText('Step 1: Connect to Serial (not connected)')





    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        pathName= QtWidgets.QFileDialog.getExistingDirectory(self, "STEP 1, Choose Folder to Save", self.defaultPath,options=options)
        self.defaultPath=pathName
        # print(pathName[-4:])
        if pathName:
            pathName += time.strftime("/%Y-%m-%d_%H%M%S_.csv")
            # print(pathName)
            pathName.strip()
            self.pathName = pathName[-22:]


            try:
                self.theFile=open(pathName, 'w')
                self.textBrowser.append("file ready")
                self.stepThree.setText('Step 3: Choose Folder to Save   (Chosen)')


            except Exception as e:
                self.file_status = str(e)
                self.textBrowser.append(self.file_status)


            self.fileText.setText(pathName)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prep = Luncher()
    app.exec_()
