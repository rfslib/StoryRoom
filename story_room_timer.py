"""
    File: story_room_timer.py
    Author: Ed C, et. al.

    - always running, modal mode on the control screen
    - start OBS Studio if not running already
    - verify there's sufficient disk space
    - get the output filename (create a touch keyboard on the control screen)
    - wait for the start button
    - display an on-screen timer on the monitor screen
        - countdown to Live, minutes remaining, two-minute warning, end
    - start and stop the video recording (using OBS Studio)
    - wait for and copy the video file (OBS Studio will remux it)
    - clean up and loop to top
"""

from dis import show_code
import tkinter as tk
import time

class Story_Room_Timer( ):

    debug = 1

    ## control
    txt = '<init>'
    state = 0 
    # 0 = waiting to start
    # 1 = countdown to start of recording
    # 2 = countdown to end of recording
    # 3 = waiting for remux
    # 4 = ready

     ## attributes of the timer overlay (OSD, on-screen display)
    text_color = 'DarkGrey'        # normal color of text
    text_warn_color = 'DarkRed'        # warning color of text
    text_font = 'Lucida Console'   # font for text
    text_fontsize = 64             # font size
    win_placement = '600x100+0+0' # size and position of timer window
    win_fade = 0.6                # transparency value of the background
    win_destroy = False             # set to True to self-destruct

    def __init__(self) -> None:
        print( 'story_room_timer init')

    def create_window( self ):
        self.win_destroy = False
        # set up the timer display on the monitor (OBS calls it a 'Projector')
        self.win = tk.Tk( )
        #self.win.geometry( self.win_placement )
        self.win.attributes( '-alpha', self.win_fade )
        self.win.overrideredirect( True )
        #self.win.grid( )
        if self.debug: self.win_exb = tk.Button( self.win, text = 'debug exit', 
            command = self.exit_class ).grid( column = 1, row = 0 )
        self.show_text( '<init>' )
        if self.debug: print( 'timer ready' )
        self.update_timer_display( )
        # self.win.mainloop( ) # the main class does the main loop :)

    def destroy_window( self ):
        self.win_destroy = True

    def show_text( self, str ):
        tk.Label( self.win, text = str,
            font = ( self.text_font, self.text_fontsize ), 
            fg = self.text_color ).pack().grid( column = 0, row = 0 )
 
    def timer_waiting( self ):
        self.txt = 'waiting'

    def update_timer_display( self ):
        self.show_text( self.txt )
        if self.win_destroy:
            self.win.destroy()
        else:
            self.win.after( 1000, self.update_timer_display )

    def exit_class( self ):
        """
        This is only used for development/debugging
        """
        self.win.destroy()
        if self.debug: print( 'timer destroyed' )

   
tst = Story_Room_Timer()