#!/usr/bin/python

import itertools
import sys,getopt,glob
from serial.tools import list_ports
import serial
import time
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
import mysql.connector


argv=sys.argv[1:]
inputfile = ''
outputfile = ''
#print(sys.version)

def read_serial(Port):
    index=0
    out=[]
    while Port.inWaiting() > 0:
        out.append(Port.read(1))
        index+=1

    tran_stamp=time.now()
    return out




###### grab input strings #######
try:
    opts, args = getopt.getopt(argv, "hp:s:", ["ii=", "oo="])
except getopt.GetoptError:
    print('test.py -p <port> -s <Session>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('test.py -p <port> -s <Session>')
        sys.exit()
    elif opt in ("-p", "--port"):
        port = arg
    elif opt in ("-s", "--session"):
        sess_ID = arg
try:
    print('Session '+sess_ID+' Attempt '+port)
except NameError:
    print('test.py -p <port> -s <Session>')
    sys.exit(2)


##### Actually #####
if __name__ == "__main__":
    print("yoniii")
    while 1:







class Station:  # each Station can have multiple Sessions
    def __init__(self):
        self.cnx = mysql.connector.connect(user='dennis', password='rh960615',
                              host='ssh.dennisren.com',
                              database='Salk')  # connect to Database
        Sessions=[]
    def start_station(self):
        for session in Sessions:
            p = multiprocessing.Process(target=session.start, args=(i,))

    def __init__(self,Com_Port):
        self.ComPort = serial.Serial(Com_Port)  # open the COM Port
        self.ComPort.baudrate = 9600  # set Baud rate
        self.ComPort.bytesize = 8  # Number of data bits = 8
        self.ComPort.parity = 'N'  # No parity
        self.ComPort.stopbits = 1  # Number of Stop bits = 1
    def start(self):
        while ComPort.inWaiting() > 0:
            out.append(Port.read(1))
            index += 1


