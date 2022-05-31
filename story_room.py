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

# Tk event callback
def callback_test( ):
    print( 'callback called :)')
    timer_win.set_txt( 'YAY!')
    timer_win.start_countdown( 'remaining minutes: {}', 120, 60, 60, callback_test )

#set up window manager
wm = Tk()

if debug: # show the root window so it can be closed to exit the test
    wm.geometry( '400x100+0+48' )
    wm.title( 'Close me to shut down the test' )
else: # but normally hide the root window
    wm.withdraw()

control_win = Control_Window( wm )

timer_win = Timer_Window( wm )
timer_win.set_txt( 'waiting' )

# timer_win.start_countdown( 'starting in {} seconds', 5, 1, 3, callback_test )

wm.mainloop() # make Tk work


