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
    txt = 'starting'
    state = 0 
    # 0 = waiting to start
    # 1 = countdown to start of recording
    # 2 = countdown to end of recording
    # 3 = waiting for remux
    # 4 = ready

     ## attributes of the timer overlay (OSD, on-screen display)
    text_color = 'red' #'DarkGrey'        # normal color of text
    text_warn_color = 'DarkRed'        # warning color of text
    text_font = 'Lucida Console'   # font for text
    text_fontsize = 64             # font size
    win_placement = '600x100+0+0' # size and position of timer window
    win_fade = 0.4                # transparency value of the background
    win_destroy = False             # set to True to self-destruct

    def __init__(self) -> None:
        print( 'story_room_timer init')

    def create_window( self ):
        self.win_destroy = False
        # set up the timer display on the monitor (OBS calls it a 'Projector')

        # create the main window
        self.win = tk.Tk( )
        self.win.geometry( self.win_placement )
        self.win.attributes( '-alpha', self.win_fade )
        self.win.overrideredirect( True )

        self.foo = tk.Label( master=self.win, text=self.txt )

        if self.debug: self.win_exb = tk.Button( master=self.win, text = 'X', bg='red',
            command = self.exit_class ).pack()
        self.txt='<init>'
        if self.debug: print( 'timer ready' )
        self.update_timer_display( )
        #self.win.mainloop( ) # the main class does the main loop :)

    def destroy_window( self ):
        self.win_destroy = True

    def show_text( self ):
        self.foo.config( text=self.txt )
        self.foo.pack()
 
    def timer_waiting( self ):
        self.txt = 'waiting'

    def update_timer_display( self ):
        self.show_text( )
        if self.debug: print( f'txt="{self.txt}"')
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

if __name__ == '__main__':   
    tst = Story_Room_Timer()
    tst.create_window()
    tst.win.mainloop()