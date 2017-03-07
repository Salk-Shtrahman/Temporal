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
from multiprocessing import Process, Value, Array, Manager
from Grinder import *
import serial
lor=[]
tof=[]


# import plotly.plotly as py
# import plotly.tools as tls
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api








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

    temp = patches.Rectangle(
        (1, 1),  # (x,y)
        .01,  # width
        1,  # height
    )

    del_but1 = []
    del_but2 = []
    del_but3 = []
    del_but1.append(ax3.add_patch(copy.copy(temp)))
    del_but2.append(ax4.add_patch(copy.copy(temp)))
    del_but3.append(ax4.add_patch(copy.copy(temp)))
    tempy = []
    a_tempy=[]
    new_stuff = Value('b', False)
    dump = Array('i', range(3))
    timestampd = Value('f', 0.0)
    songdump = Array('i', range(4))
    manager = Manager()
    lickdump = manager.list()
    lickdirection = manager.list()
    time.sleep(2)
    slave = Process(target=Serial_Process, args=(lickdirection, dump, lickdump, songdump, timestampd, new_stuff))
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
        ld=lickdirection[:]
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
        tempy=[]
        a_tempy=[]
        for eventee,l in zip(event_time,ld ):
            tempy.append(patches.Rectangle(
                (eventee, -1 if l==0 else 0),  # (x,y)
                .01,  # width
                1,  # height
            ))
        # print(tempy)
    #    print(temp.get_axes())
        for term in tempy: a_tempy.append(copy.copy(term))
        bar_cache.insert(0, a_tempy)#load up history list
        if len(bar_cache) == 4:
            bar_cache.pop()
            #   print(bar_cache[0].get_axes())
        del_but1=[]
        for term in a_tempy:
            del_but1.append(ax3.add_patch(term))  #return delete button
        # print("delete time!!")
        # print(del_but1)
        plt.pause(0.001)

        print(del_but2)
        try:  # get rid of whatever was there
            for dell in del_but2:
                dell.remove()
        except TypeError:
            del_but2.remove()
        except Exception as e:
            print(str(e))

        try:
            inst1=[]
            del_but2=[]
            for term in bar_cache[1]:
                inst1.append(copy.copy(term))
                print(inst1[::-1][0])
                ass=ax4.add_patch(inst1[::-1][0])
                del_but2.append(ass)
            #     print(inst1.get_axes())
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
        except Exception as e:
            print(str(e))

        try:
            inst2 = []
            del_but3 = []
            for term in bar_cache[2]:
                inst2.append(copy.copy(term))
                del_but3.append(ax5.add_patch(inst2[::-1][0]))

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
