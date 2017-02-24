import time
import random
import math
import matplotlib
matplotlib.use('QT5Agg')
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import copy
from multiprocessing import Process, Value, Array
lor=[]
tof=[]


# import plotly.plotly as py
# import plotly.tools as tls
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
class Grind():
    def __init__(self):
        self.count=1
    def read_serial(self):

        #print(self.count)
        if self.count == 1:
            time.sleep(3)
            payload=self.count, time.time()# new event tag
        if self.count==2:
            time.sleep(1.2)
            payload= self.count, random.randint(0,3),random.randint(0,3),random.randint(0,3), random.randint(0,3) #Song
        if self.count == 3:
            time.sleep(random.randint(20,80)/100)
            payload= self.count, time.time()#timestamp
        if self.count == 4:
            time.sleep(1)
            payload= self.count, random.randint(-1, 1),random.randint(0, 1) #right/wrong
        if self.count == 5:
            time.sleep(.1)
            payload= self.count, random.randint(0, 16)
        self.count = self.count + 1 if self.count < 5 else 1
        return payload
# Type 1 Transmission: Session start Session_Id ++
# Type 2 Transmission: End of Phase 1, tone info cdef
# Type 3 Transmission: Event trigger, 1f - left, 1e - right
# Type 4 Transmission: End of Phase 2, lick info, correct/ incorrect info
# Type 5 Transmission: Difficulty

def Serial_Process(pcc,idump,lickdump,songdump,timestampd,new_stuff):
    print("thread started")

    event_time = []
    while 1:

        result = pcc.read_serial()
        print(result)
        type = result[0]
        if type == 1:
            t_zero = result[1]
        if type == 2:
            song=result[1:4]
        if type == 3:
            event_time.append(result[1] - t_zero)
            print('Lick time= %f' % event_time[::-1][0])

        if type == 4:  # type==4:
            direction = result[1]
            correct = result[2]

        if type == 5:  # plot difficulty
            difficulty=result[1]

            idump[0]=direction
            idump[1]=correct
            idump[2]=difficulty
            for i in range(len(event_time)):
                lickdump[i]=event_time[i]
            # print(event_time[:])
            # print(lickdump[:])
            songdump=song
            timestampd=t_zero
            event_time = []
            new_stuff.value=True

p = Grind()




tlor=0
ttof=0
ind=1
# Type 1 Transmission: Session start Session_Id ++
# Type 2 Transmission: End of Phase 1, tone info cdef
# Type 3 Transmission: Event trigger, 1f - left, 1e - right
# Type 4 Transmission: End of Phase 2, lick info, correct/ incorrect info
# Type 5 Transmission: Difficulty
l_diff=[0,]
bar_cache=[]
event_time=[]



if __name__ == '__main__':

    print("I'm in")

    fig1 = plt.figure(1)
    plt.ion()
    ax1 = fig1.add_subplot(211)
    ax1.set_autoscale_on(False)
    plt.ion()
    plt.yticks([-1, 0, 1], ['Left', 'No lick', 'Right'])
    ax2 = fig1.add_subplot(212)
    ax2.grid(True)
    ax2.xaxis.grid(True)
    del_but0 = ax2.step(1, 1)

    #### the second figure window

    fig2 = plt.figure(2)
    plt.ion()
    ### first guy
    ax3 = fig2.add_subplot(311)
    plt.xlim(0, 3)
    plt.ylim(-1, 1)
    plt.title('Most recent')
    plt.yticks([-1, 0, 1], ['Left', 'No lick', 'Right'])
    ax3.axhline(y=0, color='k')
    ### second guy
    ax4 = fig2.add_subplot(312)
    plt.xlim(0, 3)
    plt.ylim(-1, 1)
    plt.title('Last Trail')
    plt.yticks([-1, 0, 1], ['Left', 'No lick', 'Right'])
    ax4.axhline(y=0, color='k')
    ### third guy
    ax5 = fig2.add_subplot(313)
    plt.xlim(0, 3)
    plt.ylim(-1, 1)
    plt.title('2 Trails Ago')
    plt.yticks([-1, 0, 1], ['Left', 'No lick', 'Right'])
    ax5.axhline(y=0, color='k')
    fig2.subplots_adjust(hspace=.75)
    plt.pause(0.01)


    new_stuff = Value('b', False)
    dump = Array('i', range(3))
    timestampd = Value('f', 0.0)
    songdump = Array('i', range(4))
    lickdump =Array('f', range(5))
    time.sleep(2)
    slave = Process(target=Serial_Process, args=(p, dump, lickdump, songdump, timestampd, new_stuff))
    slave.start()

    while 1:
        while not new_stuff.value:pass
        new_stuff.value=False
    # idump = [direction, correct, difficulty]
    # lickdump = event_time
    # songdump = song
    # timestampd = t_zero
        t_zero=timestampd.value
        song=songdump
        event_time= lickdump[:]
        direction= dump[0]
        correct= dump[1]
        difficulty= dump[2]

        print("bro watch outtttttttttt")
        print(event_time)
        print(dump[:])
    ########################### Update color bar graph
        print(ind)
        plt.figure(1)
        plt.subplot(211)
        #result[1]
        fill="red" if correct else "green"
       # print(fill)
        ax1.add_patch(
            patches.Rectangle(
                (ind-1, -1 if direction==-1 else 0),  # (x,y)
                1,  # width
                0.01 if direction == 0 else 1,  # height
                facecolor=fill,
            )
        )
        plt.xlim(0, ind+1)
        plt.pause(0.001)

    ###################### Update difficulty graph
        l_diff.append(difficulty)
        plt.subplot(212)
        now = time.time()
       # print(list(range(ind+1)), difficulty)
        try:  # get rid of whatever was there
            for dell in del_but0:
                dell.remove()
        except TypeError:
            del_but0.remove()
        except NameError:
            pass

        del_but0=ax2.step(list(range(ind+1)), l_diff)

        plt.xlim(0, ind + 1)
        plt.ylim(0, 16)
        plt.pause(0.001)

                # after plot difficulty, also plot lick window
        plt.figure(2)
        plt.subplot(311)
        plt.title('Most Recent #%d' % ind)
        try: # get rid of whatever was there
            for dell in del_but1:
                dell.remove()
        except TypeError:
            del_but1.remove()
        except NameError:
            pass

        print(direction)
        temp=patches.Rectangle(
            (event_time[0], -1 if direction==-1 else 0),  # (x,y)
            .01,  # width
            0 if direction==0 else 1,  # height
        )
    #    print(temp.get_axes())

        bar_cache.insert(0,copy.copy(temp))#load up history list
        if len(bar_cache) == 4:
            bar_cache.pop()
            #   print(bar_cache[0].get_axes())
        del_but1=ax3.add_patch(temp)  #return delete button

        plt.pause(0.001)

        plt.subplot(312)

        try:  # get rid of whatever was there
            for dell in del_but2:
                dell.remove()
        except TypeError:
            del_but2.remove()
        except NameError:
            pass

        try:
            inst1= copy.copy(bar_cache[1])
            #     print(inst1.get_axes())
            del_but2=ax4.add_patch(inst1)
            plt.title('Last Trail #%d' % (ind - 1))
        except IndexError:
            print("312 exception")
            pass;
        plt.pause(0.001)

        plt.subplot(313)

        try:  # get rid of whatever was there
            for dell in del_but3:
                dell.remove()
        except TypeError:
            del_but3.remove()
        except NameError:
            pass

        try:
            inst2 = bar_cache[2]
            del_but3=ax5.add_patch(inst2)
            plt.title('2 Trails Ago #%d' % (ind-2))
        except IndexError:
            print("313 exception")
            pass
        plt.pause(0.001)
        ind += 1 # always at the end of the loop


    # plotly_fig = tls.mpl_to_plotly( mpl_fig )
    #
    # plotly_fig["data"][0]["marker"]["color"] = ["rgba(255,0,0,0.5)",
    #                                             "rgba(0,255,0,0.5)",
    #                                             "rgba(0,0,0,255,0.5)",
    #                                             "rgba(122,122,122,0.7)",
    #                                             "rgba(0,122,122,0.5"]
    # plot_url = py.plot(plotly_fig, filename='bars-with-multiple-colors')
