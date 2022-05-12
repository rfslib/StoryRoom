"""
    file: story_room.py
    author: Ed C

    references:
        https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python

    purpose: start Tk and set up windows for control of the Story Room recording system
            meant to run continuously
"""

from tkinter import *
from control_window import Control_Window
from timer_window import Timer_Window

debug = 1

root = Tk()

if debug: # show the root window so it can be closed to exit the test
    root.geometry( '400x100+0+0' )
    root.title( 'Close me to shut down the test' )
else: # but normally hide the root window
    root.withdraw()

control_win = Control_Window( root )

#timer_win = Timer_Window( root )

root.mainloop() # make Tk work