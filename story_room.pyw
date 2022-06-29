"""
    file: story_room.pyw
    author: Ed C

    references:
        https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python
        obs websocket doc: https://github.com/obsproject/obs-websocket/blob/4.x-current/docs/generated/protocol.md
        simple xface to obs websocket: https://github.com/IRLToolkit/simpleobsws/tree/simpleobsws-4.x (included, since pip installs an incompatible version)
        starting a process from Python: https://docs.python.org/3/library/subprocess.html

    purpose: start Tk and set up windows for control of the Story Room recording system
            meant to run continuously
"""

# TODO: Configuration File


#from tkinter import *
import tkinter as tk

# our classes for the two windows
from control_window import Control_Window

from time import sleep

import psutil
import subprocess

from sr_parm import SR_Parm as parms

debug = 1

def is_process_running( processName ): # https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            return False

#set up window manager
wm = tk.Tk()

# root window
wm.geometry( '400x300+24+24' )
wm.title( 'Story Room System starting' )

tx = tk.Text(wm, height=300, width= 250)
tx.grid( row=1, column=1, padx=4, pady=4 )
tx.insert( tk.END, 'Story Room System starting....\n')
tx.update()

# TODO: be sure OBS is running
if is_process_running(parms.obs_processname):
    tx.insert( tk.END, 'OBS is running\n')
    tx.update()
else:
    tx.insert( tk.END, 'Need to start OBS\n')
    # TODO: needs environment/context, plus need to wait until it is fully running
    try:
        subprocess.Popen(parms.obs_command, cwd=parms.obs_directory)
        sleep(5)
    except:
        tx.insert( tk.END, 'Could not start OBS. ABORTING\n')
        tx.update()
        sleep( 5 )
        exit( )

tx.insert( tk.END, 'Creating the Control Window\n')
tx.update()

control_win = Control_Window(wm)

tx.insert( tk.END, 'Initialization complete\n')
tx.insert( tk.END, '\nUse the Control Window now')
tx.update()

# hide the root window unless developing/debugging
if not debug:
    wm.withdraw()

wm.mainloop() # make Tk work
