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
        self.LOR={0:0,2:-1,1:1}
        self.event_list=[]
        self.event_dir_list = []
        self.return_new_trail = False
        self.payload_cue = False

        self.Port = serial.Serial(george)  # open the COM Port
        self.Port.baudrate = 19200  # set Baud rate
        self.Port.bytesize = 8  # Number of data bits = 8
        self.Port.parity = 'N'  # No parity
        self.Port.stopbits = 1  # Number of Stop bits = 1
        # 0     x = no        lick, 1        x = incorrect        lick, 2        x = correct        lick        #
    def flow_control(self,start_pause):
        if start_pause:
            self.Port.write(b'\x55')
            print("0x55 sent to board")
        else:
            self.Port.write(b'\x56')
            print("0x56 sent to board")
    def flush_control(self,flush_stop):
        if flush_stop:
            self.Port.write(b'\x88')
            print("0x88 sent to board")
        else:
            self.Port.write(b'\x89')
            print("0x89 sent to board")
    def read_serial(self):

        index=0
        out=[]
        KEY={b'\xfe':5, b'\xfd':10} # <-- left and right respectively




        consecutive=False

        if self.payload_cue:
            self.payload_cue=False
            return self.cued_payload

        while self.Port.inWaiting() > 0:
            buf=self.Port.read(1)

 
            if buf==b'\x77':
                print("mission successful")
            if buf==b'\x75':
                print("mission unsuccessful")
            else:
                print("POOOOOOOOOOOOOOOOOOOOOOOOOOOP")

                
            if buf:
                out.append(buf)
            else:
                return
            index+=1
        # print(self.return_song)
        print('Ladder',self.char_ladder)
        for yo in out:
            print(yo)



            
            # print(self.char_ladder)
            if yo==b'\xfe' or yo==b'\xfd':
                if len(out)==1:
                    return( 3, time.time(),1 if yo==b'\xfd' else 0)
                # try:
                #     for o in out:
                #         nobro=KEY[o]
                #     return (3, time.time(), 1 if out[0] == b'\xff' else 0)
                # except KeyError:
                #     print('super jackpottttttttttttttttttttttttttttt')
                #     if out[1]==b'\x74':
                #         print(out)
                #         while len(out) < 4:
                #             buf = self.Port.read(1)
                #             if buf:
                #                 out.append(buf)
                #         print(out)
                #         self.payload_cue=True
                #         self.cued_payload=(4, self.LOR[int.from_bytes(out[2], byteorder='big') % 16], self.COR[
                #             int.from_bytes(out[2], byteorder='big') // 16], int.from_bytes(out[3], byteorder='big'))
                #         print('jackpot just got bigger')
                #         self.char_ladder = 0
                #         return (3, time.time(), 1 if out[0] == b'\xff' else 0)

            elif self.char_ladder==0 and yo==b'\x71':
                self.char_ladder=1
                self.sesh_timeF=time.time()
                self.sesh_timeS=datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")
                self.return_new_trail=True
                self.event_list = []
                print('made it to 0')
            elif self.char_ladder==1 or self.char_ladder ==2:
                self.session_num_temp.append(yo)
                self.char_ladder+=1
                print('made it to 1,2')

            elif self.char_ladder==3 and yo==b'\x72':
                self.char_ladder = 4
                print('made it to 3')
                #do shits to varify above
            elif self.char_ladder>=4 and self.char_ladder <=9:
                self.session_song_temp.append(yo)
                self.char_ladder += 1
                print('made it to '+str(self.char_ladder))


            elif self.char_ladder==10 and yo==b'\x74':
                self.char_ladder=11
                print('made it to 10')
                # do shits to varify above
            elif self.char_ladder == 11:
                self.char_ladder = 12
                self.correct = int.from_bytes(yo, byteorder='big') // 16
                self.direction = int.from_bytes(yo, byteorder='big') % 16
                print('made it to 11')
                # print('yo',yo)
                # print('corr, dir',correct,direction)
            elif self.char_ladder == 12:
                difficulty = int.from_bytes(yo, byteorder='big')
                self.char_ladder=0
                print('made it to 12')
                if self.return_lick:
                    self.return_lick=False
                    return (4,  self.LOR[self.direction], self.COR[self.correct], difficulty)




        if self.return_new_trail:
            self.return_new_trail = False
            # print(self.session_num_temp)
            try:
                high_byte=int.from_bytes(self.session_num_temp[0], byteorder='big')<<8
                low_byte=int.from_bytes(self.session_num_temp[1], byteorder='big')
            except IndexError:
                print('jackpooooottttttttttttt',out,)
                self.return_new_trail = True
                return [5]
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
                return(1, self.sesh_timeF, self.sesh_timeS)
        elif self.return_song:
            self.return_song=False
            self.return_lick=True
            try:
                tone1 =int.from_bytes(self.session_song_temp[0], byteorder='big')
                tone2 =int.from_bytes(self.session_song_temp[1], byteorder='big')
                tone3 =int.from_bytes(self.session_song_temp[2], byteorder='big')
                tone4 =int.from_bytes(self.session_song_temp[3], byteorder='big')
                tone5 =int.from_bytes(self.session_song_temp[4], byteorder='big')
                tone6 =int.from_bytes(self.session_song_temp[5], byteorder='big')

                self.session_song_temp=[]
                return(2,tone1,tone2,tone3,tone4,tone5,tone6)
            except Exception as e:
                print(str(e)+'fuck is this you?')
                self.return_song = True





        print("------------------", self.char_ladder,out)


   ###sequencer
        return (0)





if __name__ == '__main__':


    bro=brother('COM9')
    while 1:
    #    theStartTime = time.time()
        ID_data=bro.read_serial()
        print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',ID_data)
        #


    # let's wait one second before reading output (let's give device time to answer)
    #read_ID
    # ComPort.close()                  # Close the COM self.Port


