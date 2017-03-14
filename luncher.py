# -*- coding: utf-8 -*-
from serial.tools import list_ports
import fnmatch
import serial
import mysql.connector
import time,sys,json
import csv
from settings import Settings
# Form implementation generated from reading ui file 'luncherUI.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Luncher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settingsWidget = Settings('COM4',mode=2)
        self.setupUi(self)


        ports = list(list_ports.comports())
        for p in ports:
            self.serialDrop.addItem(str(p))

        self.fileButton.clicked.connect(self.saveFileDialog)
        self.serialButton.clicked.connect(self.openSerial)
        self.sqlButton.clicked.connect(self.openSQL)
        self.lunchButton.setEnabled(False)
        self.lunchButton.clicked.connect(self.gtfo)
        self.lunchButton.setAutoDefault(True)

        self.userText.setText(self.settingsWidget.jsettings['session_default']['db_login'])
        self.passText.setText(self.settingsWidget.jsettings['session_default']['db_pass'])
        self.dbText.setText(self.settingsWidget.jsettings['session_default']['db_schema'])
        self.ipText.setText(self.settingsWidget.jsettings['session_default']['db_url'])
        self.defaultPath=self.settingsWidget.jsettings['session_default']['path']

        self.show()
        self.broImReady=[0,0,0]


    def gtfo(self):
        self.settingsWidget.jsettings['session_default']['db_login']    =self.userText.text()
        self.settingsWidget.jsettings['session_default']['db_pass']     =self.passText.text()
        self.settingsWidget.jsettings['session_default']['db_schema']   =self.dbText.text()
        self.settingsWidget.jsettings['session_default']['db_url']      =self.ipText.text()
        self.settingsWidget.jsettings['session_default']['path'] = self.defaultPath

        self.settingsWidget.jsettings['mcu_config']['drip_delay_time'] = self.settingsWidget.dripBox.value()
        self.settingsWidget.jsettings['mcu_config']['punishment_duration'] = self.settingsWidget.punishBox.value()
        self.settingsWidget.jsettings['mcu_config']['delay_duration'] = self.settingsWidget.delayBox.value()
        self.settingsWidget.jsettings['mcu_config']['tone_duration'] = self.settingsWidget.toneBox.value()
        self.settingsWidget.jsettings['mcu_config']['time_between_tones'] = self.settingsWidget.betweenToneBox.value()
        self.settingsWidget.jsettings['mcu_config']['valve_open_time'] = self.settingsWidget.valveBox.value()
        self.settingsWidget.jsettings['mcu_config']['lickwindow_duration'] = self.settingsWidget.lickBox.value()
        self.settingsWidget.jsettings['mcu_config']['trial_number'] = self.settingsWidget.trailBox.value()
        self.settingsWidget.jsettings['mcu_config']['min_difficulty'] = self.settingsWidget.minBox.value()
        self.settingsWidget.jsettings['mcu_config']['max_difficulty'] = self.settingsWidget.maxBox.value()
        self.settingsWidget.jsettings['mcu_config']['training_phase'] = 1 if self.settingsWidget.p1Button.isChecked() and self.settingsWidget.p2Button.isChecked() else 2
        self.settingsWidget.jsettings['session_default']['position'] += 1
        if self.settingsWidget.jsettings['session_default']['position'] == 5:
            self.settingsWidget.jsettings['session_default']['position'] = 1
        self.settingsWidget.ComPort=self.portName


        with open('settings.json', 'w') as outfile:
            json.dump(self.settingsWidget.jsettings, outfile)
        try:
            self.settingsWidget.download()
            self.close()
        except Exception as e:
            print('Download Failure: '+ str(e))


        self.close()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(606, 413)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_2.addWidget(self.line_5, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.stepOne = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stepOne.setFont(font)
        self.stepOne.setObjectName("stepOne")
        self.gridLayout.addWidget(self.stepOne, 0, 0, 1, 1)
        self.stepThree = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stepThree.setFont(font)
        self.stepThree.setObjectName("stepThree")
        self.gridLayout.addWidget(self.stepThree, 9, 0, 1, 1)
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
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 12, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 11, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 8, 0, 1, 1)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.serialDrop = QtWidgets.QComboBox(Form)
        self.serialDrop.setObjectName("serialDrop")
        self.horizontalLayout.addWidget(self.serialDrop)
        self.serialButton = QtWidgets.QPushButton(Form)
        self.serialButton.setObjectName("serialButton")
        self.horizontalLayout.addWidget(self.serialButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fileText = QtWidgets.QLineEdit(Form)
        self.fileText.setObjectName("fileText")
        self.horizontalLayout_3.addWidget(self.fileText)
        self.fileButton = QtWidgets.QPushButton(Form)
        self.fileButton.setObjectName("fileButton")
        self.horizontalLayout_3.addWidget(self.fileButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 10, 0, 1, 1)
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
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.lunchButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
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
        #self.settingsWidget = QtWidgets.QWidget(Form)
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
        self.stepOne.setText(_translate("Form", "Step 1: Connect to Serial"))
        self.stepThree.setText(_translate("Form", "Step 3: Choose File to Save"))
        self.label_4.setText(_translate("Form", "Choose one or both below (2 alone, 3 alone, or 2 and 3)"))
        self.stepTwo.setText(_translate("Form", "Step 2: Connect to Database"))
        self.label_6.setText(_translate("Form", "User"))
        self.userText.setText(_translate("Form", "dennis"))
        self.label_7.setText(_translate("Form", "Pass"))
        self.passText.setText(_translate("Form", "rh960615"))
        self.label_8.setText(_translate("Form", "Database"))
        self.dbText.setText(_translate("Form", "Salk"))
        self.serialButton.setText(_translate("Form", "Connect"))
        self.fileButton.setText(_translate("Form", "Browse"))
        self.label_5.setText(_translate("Form", "ServerAddress"))
        self.ipText.setText(_translate("Form", "ssh.dennisren.com"))
        self.sqlButton.setText(_translate("Form", "Connect"))
        self.lunchButton.setText(_translate("Form", "Launch"))
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
        self.textBrowser.append((self.sql_status))




    def openSerial(self):
        if self.serialButton.text()=='Connect':
            info=self.serialDrop.currentText()
            filtered_wip = fnmatch.filter([info.split(' ', 1)[0]], 'COM?*')[0]
            self.portName=filtered_wip
            # print(filtered_wip)
            try:
                self.ComPort = serial.Serial(filtered_wip)  # open the COM Port
                self.ComPort.baudrate = 9600  # set Baud rate
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
                self.broImReady[2] = 1
                self.lunchButton.setEnabled(sum(self.broImReady) == 3)

            except Exception as e:
                self.file_status = str(e)
                self.textBrowser.append(self.file_status)


            self.fileText.setText(pathName)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prep = Luncher()
    app.exec_()
