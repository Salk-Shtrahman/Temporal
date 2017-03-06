from __future__ import print_function
import serial
import binascii
import time
import threading
import os
from datetime import date, datetime, timedelta
import mysql.connector



#READER_MODE 00=single 01=cont nromal 10=cont line 11 return SW version
def read_ID(Port):

   time.sleep(1)
   index=0
   out=[]
   while Port.inWaiting() > 0:
     out.append(Port.read(1))
     index+=1
   print(out)
   print("------------------")
   return (out)





import struct# import pySerial module
ComPort = serial.Serial('COM4') # open the COM Port
ComPort.baudrate = 20800         # set Baud rate
ComPort.bytesize = 8             # Number of data bits = 8
ComPort.parity   = 'N'           # No parity
ComPort.stopbits = 1             # Number of Stop bits = 1
cnx = mysql.connector.connect(user='dennis', password='rh960615',
                              host='ssh.dennisren.com',
                              database='Salk')
cursor=cnx.cursor()
cursor.execute(
    "INSERT INTO  Temporal_Trails ( Session_ID, Trail_ID, SequenceStartTime, Song, LickTime, Difficulty, Correctness, LickResult) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
    ( 1, 1,'1', '1', '1', 1, 1, 1))
cnx.commit()

while 1:
#    theStartTime = time.time()
    ID_data=read_ID(ComPort)
    #
    #shamelist below, gives bad boys a non-repeat penalty

#
#write new query to upload incident
#checkDB for today's data
#determine wheather animal is permitted to enter
#if deniad, do something
#if approved, open door, proceed with sequence


# let's wait one second before reading output (let's give device time to answer)
#read_ID
ComPort.close()                  # Close the COM Port


