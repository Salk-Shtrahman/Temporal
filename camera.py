# -*- coding: utf-8 -*-
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtMultimedia import (QAudioEncoderSettings, QCamera,
        QCameraImageCapture, QImageEncoderSettings, QMediaMetaData,
        QMediaRecorder, QMultimedia, QVideoEncoderSettings)
from PyQt5.QtCore import QByteArray, qFuzzyCompare, Qt, QTimer
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QDialog,
        QMainWindow, QMessageBox, QWidget)

import sys
# Form implementation generated from reading ui file 'luncherUI.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Camera(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.setupUi()
        cameraDevice = ''
        videoDevicesGroup = QActionGroup(self)
        videoDevicesGroup.setExclusive(True)

        for deviceName in QCamera.availableDevices():
            description = QCamera.deviceDescription(deviceName)
            videoDeviceAction = QAction(description, videoDevicesGroup)
            videoDeviceAction.setCheckable(True)
            videoDeviceAction.setData(deviceName)

            if not cameraDevice:
                cameraDevice = deviceName
                videoDeviceAction.setChecked(True)
        print(7)
        self.setCamera(cameraDevice)
        print(8)
        self.show()

    def setupUi(self):
        self.gridLayout_3 = QtWidgets.QGridLayout(self)
        self.viewfinder = QCameraViewfinder()

        self.gridLayout_3.addWidget(self.viewfinder, 0, 0, 1, 1)

    def setCamera(self, cameraDevice):
        if cameraDevice.isEmpty():
            self.camera = QCamera()
        else:
            self.camera = QCamera(cameraDevice)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()


    def updateCameraDevice(self, action):
        self.setCamera(action.data())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prep = Camera()
    app.exec_()
