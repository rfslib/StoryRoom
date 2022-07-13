"""
    file: control_window.py
    author: ed c
"""

# TODO: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the non-C: drive)
# TODO: get the desired filename
# TODO: check that OBS is running and start it before starting countdown to recording start
# TODO: periodically check OBS status (every nn seconds)
# TODO: check event against expected action and status
# TODO: OBS portable mode (config settings are saved in the OBS main folder) see obsproject.com/forum/resources/obs-and-obs-studio-portable-mode-on-windows.359
# TODO: OBS Event: 'SourceDestroyed', Raw data: {'sourceKind': 'scene', 'sourceName': 'Scene', 'sourceType': 'scene', 'update-type': 'SourceDestroyed'}: close app
# TODO: capture OS events (i.e., close app, etc.)
# TODO: detect USB drive, copy file at end of recording, unmount USB drive
# TODO: catch OBS events (? under what conditions? connect() has to be active)
# TODO: installer (installation instructions)
# TODO: (OBS) create sources, lock configuration files
# TODO: check, set Sources, Profile, Scene (create standards for these)
# TODO: set filename format (SetFilenameFormatting)
# TODO: QSG (have this app set all parameters so no manual settings are required)
# TODO: warn on version mismatch for OBS, websockets and simpleobsws
# TODO: USB disconnect
# DONE: disable buttons when not valid
# DONE: finish logic to abort recording (countdown to start vs middle of recording)
# DONE: button/function to stop recording early
# DONE: change to seconds remaining on final 2 minutes of recording
# DONE: warn on low disk space (use psutil.disk_usage(".").free/1024/1024/1024)
# DONE: start OBS here or a separate class instead of startup so it can be checked/started from here

import asyncio
from tkinter import *
import psutil

from sr_parm import SR_Parm as parms
from obs_xface import OBS_Xface, OBS_Error

import timer_window

free_disk = 0

class Recording_State:
    INIT = 0
    READY = 1
    COUNTDOWN = 2
    RECORDING = 3
    FINISHING = 4
    CLEANUP = 5
    ABORTING = -1

class Control_Window(Toplevel):

    debug = 1

    state = Recording_State.INIT

    # environment info
    free_disk = 0.0

    sr_version = '0.2'

    def __init__(self, master):
        Toplevel.__init__(self, master)

        self.state = Recording_State.INIT

        # set our look
        self.config(bg=parms.bgcolor)
        self.overrideredirect(True) # don't show title 
        self.attributes('-alpha', 1.0) # set transparency
        self.attributes('-topmost', 1) # stay on top

        # get our size and location
        self.mwidth = self.winfo_screenwidth()
        self.mheight = self.winfo_screenheight()
        self.moffsetx = 0
        self.moffsety = 0
        if self.debug:
            self.mwidth = int( self.mwidth / 2 ) 
            self.mheight = int( self.mheight / 2 ) 
            self.moffsetx = 48
            self.moffsety = 48
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')
        if self.debug: print( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )
        self.resizable(False, False)

        # set up the window's "title" frame
        self.ttlframe = Frame( master=self, relief = RIDGE, borderwidth=5, bg=parms.bgcolor, padx=parms.padxy, pady=parms.padxy )
        self.ttlframe.grid(row=0, column=0, columnspan=3, padx=parms.padxy, pady=parms.padxy, sticky='ew')
        self.grid_columnconfigure( 0, weight=1 )
        self.ttllbl = Label(master=self.ttlframe, text=parms.ttl, font=(parms.font_bold, parms.fontsize), bg=parms.bgcolor, fg=parms.fontcolor)
        self.ttllbl.pack(padx=parms.padxy, pady=parms.padxy)

        # create a frame for interactions (buttons, text entry, etc.)
        self.btnframe = Frame(master=self, padx=parms.padxy, pady=parms.padxy)
        self.btnframe.grid(row=2, column=0, padx=parms.padxy, pady=parms.padxy, sticky='ewn')
        self.ctrl_strt= Button(self.btnframe, text=parms.start_btn_txt, height=parms.start_btn_height, font=(parms.font_bold, parms.btn_fontsize),
            command=self.session_init)
        self.ctrl_strt.grid(row=0, column=0, padx=parms.padxy, pady=parms.padxy)
        self.ctrl_strt['state'] = DISABLED
        self.ctrl_stop= Button(self.btnframe, text=parms.stop_btn_txt, height=parms.start_btn_height, font=(parms.font_bold, parms.btn_fontsize),
            command=self.session_stop)
        self.ctrl_stop.grid(row=0, column=1, padx=parms.padxy, pady=parms.padxy)
        self.ctrl_stop['state'] = DISABLED
        self.update

        # "info" frame
        self.infoline=StringVar()
        self.diskline=StringVar()
        self.set_diskline(f'Available disk space: ????? ')
        self.infframe = Frame(master=self, bg=parms.bgcolor, padx=parms.padxy, pady=parms.padxy)
        self.infframe.grid(row=6, column=0, padx=parms.padxy, pady=parms.padxy, sticky = 'es')
        self.inflabel = Label(master=self.infframe, textvariable=self.infoline, fg=parms.info_fontcolor, font=(parms.font_family, parms.info_fontsize))
        self.inflabel.pack(padx=parms.padxy, pady=parms.padxy)
        self.dsklabel = Label(master=self.infframe, textvariable=self.diskline, fg=parms.info_fontcolor, font=(parms.font_family, parms.info_fontsize))
        self.dsklabel.pack(padx=parms.padxy, pady=parms.padxy)
        self.update()
              
        if self.debug: print('control window ready')

        # set up the timer window
        self.tw = timer_window.Timer_Window(master)
        self.tw.set_txt(parms.timer_waiting_message)
        
        if self.debug: print('timer window ready')

        # get OBS going
        self.set_infoline('Starting OBS')
        self.update()
        try:
            self.ws = OBS_Xface(host=parms.obs_host, port=parms.obs_port, password=parms.obs_pswd, callback=self.on_obs_event)
        except (OBS_Error) as err:
            print(f'When starting OBS: "{err}"')
            self.set_infoline('OBS Startup Failed. Restart the System.', text_color=parms.text_warn_color)
        else:
            self.set_infoline(f'sr: {self.sr_version}, obs: {self.ws.obs_version}, ws: {self.ws.ws_version}')
            self.show_disk_space()
            if self.debug: print('system ready')

        self.ctrl_strt['state'] = NORMAL
        self.update()

        self.state = Recording_State.READY

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
        self.state = Recording_State.COUNTDOWN
        # TODO: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the non-C: drive)
        # TODO: get the desired filename
        self.ctrl_stop['state'] = NORMAL
        self.tw.start_countdown('Start recording in {} seconds', 10, 1, 5, 0, self.session_start_recording)

    def session_start_recording( self ):
        self.state = Recording_State.RECORDING
        self.ctrl_strt['state'] = DISABLED
        self.ws.start_recording()
        self.ctrl_stop['state'] = NORMAL
        self.tw.start_countdown('Recording time remaining: {} minutes', 120, 60, 90, 60, self.session_end_warn)

    def session_end_warn(self):
        self.tw.start_countdown('Recording time remaining: {} seconds', 60, 1, 60, 0, self.session_end_recording)

    def session_end_recording(self):
        self.ctrl_stop['state'] = DISABLED
        self.ws.stop_recording()
        self.state = Recording_State.FINISHING
        self.tw.set_txt('Recording Stopped')
        # TODO: copy to USB, 
        # TODO: save to archive
        self.session_reset()

    def session_stop(self): # early stop of recording
        if self.state == Recording_State.COUNTDOWN:
            self.tw.stop_countdown(self.session_reset)
        elif self.state == Recording_State.RECORDING:
            self.tw.stop_countdown(self.session_end_recording)
        self.state = Recording_State.ABORTING
        if self.debug: print('aborting')

    def session_reset(self): # reset environment for next recording
        if self.debug: print('session_reset')
        self.ctrl_stop['state'] = DISABLED
        self.ctrl_strt['state'] = NORMAL
        self.tw.set_txt(parms.timer_waiting_message)
        self.state = Recording_State.READY

    def get_infoline( self ):
        return self.infoline.get()

    def set_infoline( self, textin, text_color=parms.text_soft_color ):
        self.inflabel.config(fg=text_color)
        self.infoline.set(str(textin))
    
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
        self.set_diskline( f'Available disk space: {self.free_disk/1024:.1f}G ' )
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
