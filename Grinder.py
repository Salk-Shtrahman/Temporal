import random,time,datetime
import mysql.connector
from experiment import brother

class Grind():
    def __init__(self):
        self.count=1
        self.sql_status='pending'
        self.badboy=4


    def read_serial(self):

        #print(self.count)
        if self.count == 1:
            time.sleep(1)
            payload=self.count, time.time(), datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")# new event tag
        if self.count==2:
            time.sleep(1.2)
            payload= self.count, random.randint(0,3),random.randint(0,3),random.randint(0,3), random.randint(0,3) #Song
        if self.count == 3:
            time.sleep(random.randint(20,80)/100)
            payload= self.count, time.time(), random.randint(0, 1)#timestamp
            if self.badboy:
                self.count-=1
                self.badboy-=1
        if self.count == 4:
            self.badboy = 4
            time.sleep(1)
            payload= self.count, random.randint(-1, 1),random.randint(0, 1), (random.randint(0, 16)*random.randint(0,1))
        self.count = self.count + 1 if self.count < 4 else 1
        return payload
# Type 1 Transmission: Session start Session_Id ++
# Type 2 Transmission: End of Phase 1, tone info cdef
# Type 3 Transmission: Event trigger, 1f - left, 1e - right
# Type 4 Transmission: End of Phase 2, lick info, correct/ incorrect info
# Type 5 Transmission: Difficulty

# class Grind_DB():

# 1	SequenceStartTime	TIME
# 2	Song	STR
# 3	LickTime	CSV(STR)
# 4	Difficulty	INT
# 5	LickResult	INT
# 6	Correctness	BOOL
def Serial_Process(port_name,lickdirection,idump,lickdump,songdump,timestampd,new_stuff):
    print("thread started")
    # cursor = cnx.cursor()
    # t_zero_que = "INSERT INTO  Temporal_Trails(Session_ID,Animal_ID,Event_Type_ID,Trail_ID,Result) VALUES (%i,%i,%i,%i)"
    event_time = []
    dirr=[]
    bro=brother(port_name)
    update_flag=False;
  #  bro=Grind()
    t_zero=time.time()
    while 1:
        # (1, 1488832244.381148, '20170306123044.381148')
        # 20170306123044.383
        # (2, 2, 6, 6, 5)
        # (3, 0, 0, 13)
        result = bro.read_serial()
        print(result)
  #      print(result)
        try:
            type = result[0]
        except Exception as e:
            print(e)
            type=result

        if type == 1:
            t_zero = result[1]
            text_time=float(result[2])

            if update_flag:
                update_flag=False
                try:

                    idump[0] = direction
                    idump[1] = correct
                    idump[2] = difficulty

                    lickdump[:] = event_time
                    lickdirection[:] = dirr
                    print('direction is important', lickdirection[:])
                    timestampd.value = text_time
                    event_time = []
                    dirr = []

                    new_stuff.value = True
                    print("####THREAD##### : Toggled")
                except Exception as e:
                    lickdump[:] = [0]
                    lickdirection[:] = [0]
                    print(e, 'ignoring this round, its garbage')

            #print(text_time)            # cursor.execute(t_zero_que, (t_zero,))
            # cnx.commit()
        if type == 2:
            song=result[1:5]
            for i in range(len(song)):
                songdump[i] = song[i]
                
        if type == 3:
            event_time.append(result[1] - t_zero)
            dirr.append(result[2])
          #  print('Lick time= %f' % event_time[::-1][0])

        if type == 4:  # type==4:
            direction = result[1]
            correct = result[2]
            difficulty = result[3]

            update_flag = True
            # for i in range(len(event_time)):





