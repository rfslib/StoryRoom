"""
    file: story_room.py
    author: Ed C

    references:
        https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python

    purpose: start Tk and set up windows for control of the Story Room recording system
            meant to run continuously
"""

from shutil import disk_usage
from time import time
from tkinter import *

# our classes for the two windows
from control_window import Control_Window
from timer_window import Timer_Window

debug = 1

#set up window manager
wm = Tk()

# root window
wm.geometry( '400x300+24+24' )
wm.title( 'System starting' )
# hide the root window unless developing/debugging
if not debug: # but normally hide the root window
    wm.withdraw()

control_win = Control_Window( wm )

wm.mainloop() # make Tk work


