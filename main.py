import serial
import mysql
from serial.tools import list_ports
import subprocess
import fnmatch
import tkinter as tk
import tkinter.font as tkFont
from multiprocessing import Pool, Lock

class Selecter(object):
    def __init__(self):
        self.root = tk.Tk()
        self.ports = list(list_ports.comports())
        # use width x height + x_offset + y_offset (no spaces!)
        self.root.geometry("%dx%d+%d+%d" % (400, 350, 250, 150))
        self.root.title("COM Port Matching")
        self.var1 = tk.StringVar(self.root)
        self.var2 = tk.StringVar(self.root)
        self.var3 = tk.StringVar(self.root)
        self.var4 = tk.StringVar(self.root)
        self.customFont = tkFont.Font(family="Helvetica", size=15)
        # initial value
        self.var1.set('Please Slect')
        self.var2.set('Please Slect')
        self.var3.set('Please Slect')
        self.var4.set('Please Slect')
        choices = self.ports

        tk.Label(self.root, text="Box #1", font=self.customFont).pack()
        option = tk.OptionMenu(self.root, self.var1, *choices)
        option.pack(side='top', padx=10, pady=10)

        tk.Label(self.root, text="Box #2").pack()
        option1 = tk.OptionMenu(self.root, self.var2, *choices)
        option1.pack(side='top', padx=10, pady=10)

        tk.Label(self.root, text="Box #3").pack()
        option2 = tk.OptionMenu(self.root, self.var3, *choices)
        option2.pack(side='top', padx=10, pady=10)

        tk.Label(self.root, text="Box #4").pack()
        option3 = tk.OptionMenu(self.root, self.var4, *choices)
        option3.pack(side='top', padx=10, pady=10)

        button = tk.Button(self.root, text="Submit", command=self.select)
        button.pack(side='top', padx=20, pady=10)
        self.root.mainloop()

    def select(self):
        print("value is %s" % self.var1.get())
        print("value is %s" % self.var2.get())
        print("value is %s" % self.var3.get())
        print("value is %s" % self.var4.get())
        self.quit()
    def quit(self):
        self.root.destroy()
    def pour(self):
        return [self.var1.get(), self.var2.get(), self.var3.get(),self.var4.get()]



#def port_select():


 #   return match


if __name__ == "__main__":
    filtered=[]
    match = ['', '', '', '']
    rooty=Selecter()
    port_list=rooty.pour()
    for port in port_list:
        filtered_wip=fnmatch.filter([port.split(' ', 1)[0]], 'COM?*')
        print(filtered_wip)
        try:
            filtered.append(filtered_wip[0])
        except AttributeError:
            filtered.append('')
        except IndexError:
            filtered.append('')
    print(filtered)
    pool = Pool()
    processes = set()
    for session, comport in enumerate(filtered):
        if comport is not '':
            processes.add(subprocess.Popen(['python', 'pySalk.py', '-p', comport, '-s', str(session + 1)]))

    while 1:
        pass





