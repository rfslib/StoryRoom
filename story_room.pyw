"""
file: story_room.pyw
author: Ed C

references: https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python

purpose: start Tk and set up windows for control of the Story Room recording system which is meant to run continuously
"""

debug = 1

import tkinter as tk
from control_window import Control_Window

sr_version = 0.2

wm = tk.Tk() # create root window
wm.geometry('400x300+24+24')
wm.title('Story Room System Startup')

tx = tk.Text(wm, height=300, width= 250)
tx.grid(row=1, column=1, padx=4, pady=4)
tx.insert(tk.END, 'Story Room System starting....\n')
tx.update()

control_win = Control_Window(wm)

tx.insert(tk.END, 'Initialization complete\n')
tx.update()

# hide the root window unless developing/debugging
if not debug:
    wm.withdraw()

wm.mainloop() # make Tk work
