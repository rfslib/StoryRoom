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

###from story_room_timer import *

class Story_Room_Control( ):

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
    ctrl_fontsize = 24              # font size
    ctrl_entry = 'set filename'     # Button text for filename entry
    ctrl_entrysize = 12             # font size for filename entry
    ctrl_bg = 'grey'                # background color
    frame_pad = 4                   # padding inside of frames


## --------    
    def __init__( self ):
        """
        https://realpython.com/python-gui-tkinter/#building-your-first-python-gui-application-with-tkinter
        """

        # create the control display so we can query the system
        self.winc = tk.Tk( )
        ###self.timer_win = Story_Room_Timer()

        # set up the control display on the control screen
        self.winc.overrideredirect( True )
        # monitor sizes change, so let's see what we have
        self.mwidth = self.winc.winfo_screenwidth( )
        self.mheight = self.winc.winfo_screenheight( )
        if not self.debug:
            self.mwidth = self.winc.winfo_screenwidth( )
            self.mheight = self.winc.winfo_screenheight( )
            self.moffsetx = 0
            self.moffsety = 0

        self.winc.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )    

        self.ttlframe = tk.Frame( master=self.winc, width = self.mwidth, relief = tk.GROOVE, borderwidth = 1, padx = self.frame_pad, pady = self.frame_pad )
        self.ttlframe.grid( row=0, column=0, padx = self.frame_pad, pady = self.frame_pad )
        tk.Label( master=self.ttlframe, text=self.ctrl_title ).pack( padx = self.frame_pad, pady = self.frame_pad)


        self.btnframe = tk.Frame( master=self.winc, width = self.mwidth, relief = tk.RIDGE, borderwidth = 1, padx = self.frame_pad, pady = self.frame_pad )
        self.btnframe.grid( row=1, column=0, padx = self.frame_pad, pady = self.frame_pad )
        tk.Label( master=self.btnframe, text='' ).pack( padx = self.frame_pad, pady = self.frame_pad)
        
        
        self.ctrl_strt= tk.Button( self.btnframe, text = 'Start Session',
                command = self.do_one,
                font = ( self.ctrl_font, self.ctrl_entrysize ) ).pack()
        if self.debug: self.ctrl_exb = tk.Button( self.btnframe, text = 'debug exit', 
                command = self.exit_class ).pack()

        if self.debug: print( 'control ready' )
        # ok, keep the screens in the loop ;)
        self.winc.mainloop( )

    def do_one( self ):
        """
        main loop, do the recording steps
        """
        # one at a time please
        if self.do_one_active: return()
        self.do_one_active = True
        if self.debug: print( 'do_one() start' )

        # initialize Session variables and timer window
        self.out_filename = ''
        self.timer_countdown = self.timer_countdown_default
        self.timer_recording = self.timer_recording_default

        ###self.timer_win.create_window()
        ###self.timer_win.txt = 'Starting'
        time.sleep( 1 )
        
        if self.debug: print( 'ready for the next session' )

        #- start OBS Studio if not running already
        if self.debug: print( 'TODO: start OBS Studio and interface')


        #- verify there's sufficient disk space
        if self.debug: print( 'TODO: verify disk space on output device')

        #- get the output filename (create a touch keyboard on the control screen)
        self.timer_win.txt = 'Filename?'
        time.sleep( 2 )
        if self.debug: print( 'TODO: get output filename')

        #- wait for the start button
        if self.debug: print( 'TODO: wait for the start button' )

        #- display an on-screen timer on the monitor screen
            #- countdown to Live, minutes remaining, two-minute warning, end
        if self.debug: print( 'TODO: start countdown to LIVE' )

        #- start and stop the video recording (using OBS Studio)
        if self.debug: print( 'TODO: start recording and countdown to end' )

        #- wait for and copy the video file (OBS Studio will remux it)
        if self.debug: print( 'TODO: wait for remux' )

        #- clean up and exit
        ###self.timer_win.destroy_window()        
        if self.debug: print( 'do_one() exit' )
        self.do_one_active = False


    
    def exit_class( self ):
        """
        This is only used for development/debugging
        """
        self.winc.destroy()
        if self.debug: print( 'control destroyed' )

app = Story_Room_Control( )
