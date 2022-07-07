"""
    file: control_window.py
    author: ed c
"""
# TODO: start OBS here or a separate class instead of startup so it can be checked/started from here
# TODO: change to seconds remaining on final 2 minutes of recording
# TODO: check that OBS is running and start it before starting countdown to recording start
# TODO: button/function to stop recording early
# TODO: check event against expected action and status
# TODO: disable buttons when not valid
# TODO: OBS portable mode (config settings are saved in the OBS main folder) see obsproject.com/forum/resources/obs-and-obs-studio-portable-mode-on-windows.359
# TODO: OBS Event: 'SourceDestroyed', Raw data: {'sourceKind': 'scene', 'sourceName': 'Scene', 'sourceType': 'scene', 'update-type': 'SourceDestroyed'}: close app
# TODO: capture OS events (i.e., close app, etc.)
# TODO: catch OBS events (? under what conditions? connect() has to be active)
# TODO: installer (installation instructions)
# TODO: (OBS) create sources, lock configuration files
# TODO: check, set Sources, Profile, Scene (create standards for these)
# TODO: set filename format (SetFilenameFormatting)
# TODO: QSG (have this app set all parameters so no manual settings are required)
# TODO: warn on version mismatch for OBS, websockets and simpleobsws
# TODO: catch errors
# TODO: USB disconnect
# DONE: warn on low disk space (use psutil.disk_usage(".").free/1024/1024/1024)

import asyncio
from tkinter import *
import psutil

from sr_parm import SR_Parm as parms
from obs_xface import OBS_Xface

import timer_window

free_disk = 0

class Control_Window(Toplevel):

    debug = 1

    # configuration stuff
    timer_waiting_message = 'Riverton Story Room'
    countdown_to_start = 20 # 20 seconds
    recording_length = 3600 # one hour of recording = 3600 seconds
    recording_warn_at = 120 # seconds before end of recording to start warning message

    # visuals
    start_btn_txt = 'Start Session'
    start_btn_height = 4
    start_btn_fontsize = 12

    ## attributes of the control window
    moffsetx = 0
    moffsety = 0
    ttl = 'Story Room'       # title
    font = 'Lucida Console'    # primary font for text
    fontsize = 48              # font size
    fontcolor = '#100010'
    bgcolor = '#efffef'             # background color
    padxy = 4                   # padding inside of frames
    info_fontsize = 10
    info_fontcolor = 'grey'
    #infoline = '' # StringVar, created in __init__, see getter and setter
    
    # OBS info
    pswd = 'family'


    # environment info
    free_disk = 0.0

    sr_version = '0.1'

    def __init__(self, master):
        Toplevel.__init__(self, master)

        # set our look
        self.config(bg=self.bgcolor)
        self.overrideredirect(True) # don't show title 
        self.attributes('-alpha', 1.0) # set transparency
        self.attributes('-topmost', 1) # stay on top

        # get our size and location
        self.mwidth = self.winfo_screenwidth()
        self.mheight = self.winfo_screenheight()
        if self.debug:
            self.mwidth = int( self.mwidth / 2 ) 
            self.mheight = int( self.mheight / 2 ) 
            self.moffsetx = 48
            self.moffsety = 48
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')
        if self.debug: print( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )
        self.resizable(False, False)

        # set up the window's "title" frame
        self.ttlframe = Frame( master=self,
            relief = RIDGE, borderwidth = 5, bg=self.bgcolor,
            padx = self.padxy, pady = self.padxy )
        self.ttlframe.grid( row=0, column=0, padx = self.padxy, pady = self.padxy, sticky='ew' )
        self.grid_columnconfigure( 0, weight=1 )
        Label( master=self.ttlframe, # width=30,
            text=self.ttl, font=('Lucida Console', self.fontsize), bg=self.bgcolor, fg=self.fontcolor,
            ).pack( padx = self.padxy, pady = self.padxy)

        # "info" frame
        self.infoline=StringVar()
        self.diskline=StringVar()
        #self.set_infoline(f'sr: {self.sr_version}, obs: {self.obs_version}, ws: {self.ws_version}')
        self.set_diskline(f'Free Disk Space: {self.free_disk / 1024:.1f}G')
        self.infframe = Frame(master=self, bg=self.bgcolor, padx=self.padxy, pady=self.padxy)
        self.infframe.grid(row=6, column=0, padx=self.padxy, pady=self.padxy, sticky = 'es')
        self.inflabel = Label(master=self.infframe, textvariable=self.infoline, fg=self.info_fontcolor, font=('Lucida Console', self.info_fontsize))
        self.inflabel.pack(padx=self.padxy, pady=self.padxy)
        self.dsklabel = Label(master=self.infframe, textvariable=self.diskline, fg=self.info_fontcolor, font=('Lucida Console', self.info_fontsize))
        self.dsklabel.pack(padx=self.padxy, pady=self.padxy)

        # create a frame for interactions (buttons, text entry, etc.)
        self.btnframe = Frame(master=self, padx=self.padxy, pady=self.padxy)
        self.btnframe.grid(row=2, column=0, padx=self.padxy, pady=self.padxy, sticky='ewn')
              
        self.ctrl_strt= Button(self.btnframe, text=self.start_btn_txt, height=self.start_btn_height, command=self.session_init, font=(self.font, self.start_btn_fontsize))
        self.ctrl_strt.pack()

        if self.debug: print('control window ready')

        # set up the timer window
        self.tw = timer_window.Timer_Window(master)
        self.tw.set_txt(self.timer_waiting_message)
        if self.debug: print('timer window ready')

    # get OBS going
        self.ws = OBS_Xface(host=parms.obs_host, port=parms.obs_port, password=parms.obs_pswd, callback=self.on_obs_event)
        if self.ws == None:
            self.set_infoline('OBS Startup Failed. Restart the System.')
        else:
            self.set_infoline(f'sr: {self.sr_version}, obs: {self.ws.obs_version}, ws: {self.ws.ws_version}')
            self.show_disk_space()
            if self.debug: print('system ready')


# ----

    async def on_obs_event(self, data):
        if data['update-type'] == 'SourceDestroyed':
            print('OBS closed so forcing exit')
            self.show_app_status('OBS closed so forcing exit')
            await asyncio.sleep( 3 )
            self.tw.destroy()
            self.destroy()
            exit(-1)
        pass # TODO: finish me

    def session_init(self):
        self.tw.start_countdown('Start recording in {} seconds', 5, 1, 5, self.session_start_recording)

    def session_start_recording( self ):
        print( 'test_callback called' )
        self.ws.start_recording()
        self.tw.start_countdown('Recording time remaining: {} minutes', 120, 60, 60, self.session_end_recording)

    def session_end_recording(self):
        self.ws.stop_recording()
        self.tw.set_txt('Recording Stopped')

    def get_infoline( self ):
        return self.infoline.get()

    def set_infoline( self, textin ):
        self.infoline.set( str( textin ) )
    
    def get_diskline(self):
        return self.diskline.get()

    def set_diskline(self, textin):
        self.diskline.set(str(textin))

    def show_disk_space(self):
        self.free_disk = psutil.disk_usage('.').free / 1024 / 1024
        print(f'free: {self.free_disk}, min:{parms.free_disk_min}')
        if self.free_disk < parms.free_disk_min:
            self.dsklabel.config( bg = parms.text_warn_color )
        else:
            self.dsklabel.config( bg = parms.bg_color )
        self.diskline.set( f'Available disk space: {self.free_disk/1024:.1f}G ' )
        self.after( parms.fd_delay, self.show_disk_space )    

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+48' )
    root.title( 'close me to exit test' )
    tst = Control_Window( root )
    #tst.start_recording( )
    #time.sleep( 3 )
    #tst.stop_recording( )
    root.mainloop()
