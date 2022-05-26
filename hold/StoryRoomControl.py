"""
    File: StoryRoomControl
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

import tkinter as tk
import time

class Control_Window( ):

    debug = 1
    do_one_active = False

    ## working
    out_filename = ''               # output filename, reset in get_ready()
    timer_countdown_default = 20    # length of time before recording starts
    timer_countdown = 20            # length of time before recording starts
    timer_recording_default = 3600  # 60 minutes of recording time
    timer_recording = 3600          # 60 minutes of recording time

    ## attributes of the console screen
    mwidth = 500
    mheight = 300
    moffsetx = 0
    moffsety = 200
    ctrl_title = 'Story Room'       # title
    ctrl_font = 'Lucida Console'    # primary font for text
    ctrl_fontsize = 48              # font size
    ctrl_fontcolor = '#100010'
    ctrl_entry = 'set filename'     # Button text for filename entry
    ctrl_entrysize = 12             # font size for filename entry
    ctrl_bg = '#efffef'             # background color
    frame_pad = 4                   # padding inside of frames


## --------    
    def __init__( self ):
        """
        https://realpython.com/python-gui-tkinter/#building-your-first-python-gui-application-with-tkinter
        """

        # create the control display so we can query the system
        self.winc = tk.Tk( )
        self.timer_win = Story_Room_Timer()
        self.winc.config( bg = self.ctrl_bg )
        # set up the control display on the control screen
        self.winc.overrideredirect( True )
        # monitor sizes change, so let's see what we have and set the display appropriately
        self.mwidth = self.winc.winfo_screenwidth( )
        self.mheight = self.winc.winfo_screenheight( )
        if not self.debug:
            self.moffsetx = 0
            self.moffsety = 0
        self.winc.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )

        # set up the title frame
        # full width: https://intellipaat.com/community/69111/python-tkinter-frame-making-frame-width-span-full-root-window-width
        self.ttlframe = tk.Frame( master=self.winc,
            relief = tk.RIDGE, borderwidth = 5, bg=self.ctrl_bg,
            padx = self.frame_pad, pady = self.frame_pad )
        self.ttlframe.grid( row=0, column=0, padx = self.frame_pad, pady = self.frame_pad, sticky='ew' )
        self.winc.grid_columnconfigure( 0, weight=1 )
        tk.Label( master=self.ttlframe, # width=30,
            text=self.ctrl_title, font=('Lucida Console', self.ctrl_fontsize), bg=self.ctrl_bg, fg=self.ctrl_fontcolor,
            ).pack( padx = self.frame_pad, pady = self.frame_pad)

        # create a frame for interactions (buttons, text entry, etc.)
        self.btnframe = tk.Frame( master=self.winc, 
            padx = self.frame_pad, pady = self.frame_pad )
        self.btnframe.grid( row=1, column=0, padx = self.frame_pad, pady = self.frame_pad, sticky='ewn' )
        tk.Label( master=self.btnframe, text='' ).pack( padx = self.frame_pad, pady = self.frame_pad )
              
        self.ctrl_strt= tk.Button( self.btnframe, text = 'Start Session',
                command = self.do_one,
                font = ( self.ctrl_font, self.ctrl_entrysize ) ).pack()

        # add a kill button if we're in development
        if self.debug:
            self.dbgframe = tk.Frame( master=self.winc )
            self.dbgframe.grid( row=4, column=0, sticky='w')
            self.ctrl_exb = tk.Button( self.dbgframe, text = 'X', command = self.exit_class, bg='red' ).pack()

        if self.debug: print( 'control ready' )
    
    def exit_class( self ):
        """
        This is only used for development/debugging
        """
        self.winc.destroy()
        if self.debug: print( 'control destroyed' )

# unit test
if __name__ == '__main__':   
    tst = Control_Window()
    print( 'control test exit' )
