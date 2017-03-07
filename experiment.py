from __future__ import print_function
import serial
import binascii
import time
import threading
import os
import mysql.connector
import binascii
import datetime



#READER_MODE 00=single 01=cont nromal 10=cont line 11 return SW version
class brother():
    def __init__(self, george):
        self.char_ladder = 0
        self.phase_ladder = 0
        self.MCU_count = []
        self.session_num_temp = []
        self.return_song = False
        self.return_lick = False
        self.session_song_temp = []
        self.COR={0:0,1:0,2:1}
        self.LOR={0:0,1:-1,2:1}
        self.event_list=[]
        self.event_dir_list = []

        self.Port = serial.Serial(george)  # open the COM Port
        self.Port.baudrate = 20800  # set Baud rate
        self.Port.bytesize = 8  # Number of data bits = 8
        self.Port.parity = 'N'  # No parity
        self.Port.stopbits = 1  # Number of Stop bits = 1
        # 0     x = no        lick, 1        x = incorrect        lick, 2        x = correct        lick        #
    def read_serial(self):

        index=0
        out=[]
        KEY={b'\xff':5, b'\xfe':10}
        return_new_trail = False
        consecutive=False
        while self.Port.inWaiting()==0:pass
        while self.Port.inWaiting() > 0:
            buf=self.Port.read(1)
            if buf:
                out.append(buf)
            else:
                return
            index+=1
        # print(self.return_song)
        for yo in out:
            # print(yo)
            # print(self.char_ladder)
            if yo==b'\xff' or yo==b'\xfe':
                if len(out)==1:
                    return( 3, time.time(),1 if yo==b'\xff' else 0)
                try:
                    for o in out:
                        nobro=KEY[o]
                    return (3, time.time(), 1 if out[0] == b'\xff' else 0)
                except KeyError:
                    pass
            elif self.char_ladder==0 and yo==b'\x71':
                self.char_ladder=1
                self.sesh_timeF=time.time()
                sesh_timeS=datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")
                return_new_trail=True
                self.event_list = []
            elif self.char_ladder==1 or self.char_ladder ==2:
                self.session_num_temp.append(yo)
                self.char_ladder+=1


            elif self.char_ladder==3 and yo==b'\x72':
                self.char_ladder = 4
                #do shits to varify above
            elif self.char_ladder==4 or self.char_ladder ==5:
                self.session_song_temp.append(yo)
                self.char_ladder += 1


            elif self.char_ladder==6 and yo==b'\x74':
                self.char_ladder=7
                # do shits to varify above
            elif self.char_ladder == 7:
                self.char_ladder = 8
                correct = int.from_bytes(yo, byteorder='big') // 16
                direction = int.from_bytes(yo, byteorder='big') % 16
                # print('yo',yo)
                # print('corr, dir',correct,direction)
            elif self.char_ladder == 8:
                difficulty = int.from_bytes(yo, byteorder='big')
                self.char_ladder=0
                self.return_lick = True
                return (4,  self.LOR[direction], self.COR[correct], difficulty)



        if return_new_trail:
            # print(self.session_num_temp)
            try:
                high_byte=int.from_bytes(self.session_num_temp[0], byteorder='big')<<8
                low_byte=int.from_bytes(self.session_num_temp[1], byteorder='big')
            except IndexError:
                print('jackpooooottttttttttttt',out)
                return
            sum = high_byte + low_byte
            # print(sum)
            try:
                self.MCU_count.pop(0)
                self.MCU_count.append(sum)
                if self.MCU_count[1]==self.MCU_count[0]+1:
                    print('consecutive')
                    consecutive=True
                else:
                    pass #deal with it later, 1f 1e injection fucked it up
            except IndexError:#the first freebee
                self.MCU_count.append(sum)
                print('consecutive')
                consecutive = True
            #clear temp
            self.session_num_temp=[]
            if consecutive:
                self.return_song = True
                return(1, self.sesh_timeF, sesh_timeS)
        elif self.return_song:
            self.return_song=False
            try:
                tone1 =int.from_bytes(self.session_song_temp[0], byteorder='big') // 16
                tone2 =int.from_bytes(self.session_song_temp[0], byteorder='big') % 16
                tone3 =int.from_bytes(self.session_song_temp[1], byteorder='big') // 16
                tone4 =int.from_bytes(self.session_song_temp[1], byteorder='big') % 16

                self.session_song_temp=[]
                return(2,tone1,tone2,tone3,tone4)
            except Exception:
                pass




        print("------------------", self.char_ladder,out)


   ###sequencer
        return ([0])





# if __name__ == '__main__':
#
#
#     bro=brother()
#     while 1:
#     #    theStartTime = time.time()
#         ID_data=bro.read_serial()
#         print('yyyyyyyyyyyyyyyyyyyyyyyyyyy',ID_data)
#         #


    # let's wait one second before reading output (let's give device time to answer)
    #read_ID
    # ComPort.close()                  # Close the COM self.Port


