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
from Grinder import *
lor=[]
tof=[]


# import plotly.plotly as py
# import plotly.tools as tls
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api


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

SONGDICT = {0:'x',1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}


if __name__ == '__main__':

    print("I'm in")

    fig1 = plt.figure(1)
    plt.ion()
    ax1 = fig1.add_subplot(211)
    ax1.set_autoscale_on(False)
    plt.ion()
    ax1.set_yticks([-1, 0, 1])
    ax1.set_yticklabels(['Left', 'No lick', 'Right'])
    ax2 = fig1.add_subplot(212)
    ax2.grid(True)
    ax2.xaxis.grid(True)
    ax2.set_ylim(0, 16)
    del_but0 = ax2.step(1, 1)

    #### the second figure window

    fig2 = plt.figure(2)
    plt.ion()
    ### first guy
    ax3 = fig2.add_subplot(311)
    ax3.set_xlim(0, 3)
    ax3.set_ylim(-1, 1)
    ax3.set_title('Most recent')
    ax3.set_yticks([-1, 0, 1])
    ax3.set_yticklabels(['Left', 'No lick', 'Right'])
    ax3.axhline(y=0, color='k')
    ### second guy
    ax4 = fig2.add_subplot(312)
    ax4.set_xlim(0, 3)
    ax4.set_ylim(-1, 1)
    ax4.set_title('Last Trail')
    ax4.set_yticks([-1, 0, 1])
    ax4.set_yticklabels(['Left', 'No lick', 'Right'])
    ax4.axhline(y=0, color='k')
    ### third guy
    ax5 = fig2.add_subplot(313)
    ax5.set_xlim(0, 3)
    ax5.set_ylim(-1, 1)
    ax5.set_title('2 Trails Ago')
    ax5.set_yticks([-1, 0, 1])
    ax5.set_yticklabels(['Left', 'No lick', 'Right'])
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
        song_alpha = []
        t_zero=timestampd.value
        song=songdump
        event_time= lickdump[:]
        direction= dump[0]
        correct= dump[1]
        difficulty= dump[2]
        song = songdump[:]
        for tone in song:
            song_alpha.append(SONGDICT[tone])
        print(song)
        print(''.join(song_alpha))

        print("bro watch outtttttttttt")
        print(event_time)
        print(dump[:])
    ########################### Update color bar graph
        print(ind)

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
        ax1.set_xlim(0, ind+1)
        plt.pause(0.001)

    ###################### Update difficulty graph
        l_diff.append(difficulty)
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

        ax2.set_xlim(0, ind + 1)

        plt.pause(0.001)

                # after plot difficulty, also plot lick window

        ax3.set_title('Most Recent #%d' % ind)
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
            ax4.set_title('Last Trail #%d' % (ind - 1))
        except IndexError:
            print("312 exception")
            pass;
        plt.pause(0.001)



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
            ax5.set_title('2 Trails Ago #%d' % (ind-2))
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
