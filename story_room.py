'''
file: story_room.py
author: rfslib

control "Story Room" recording sessions
'''

version = '20220721'

class Recording_State:
    INIT = 0
    READY = 1
    COUNTDOWN = 2
    RECORDING = 3
    FINISHING = 4
    CLEANUP = 5
    ABORTING = -1

from sr_parm import SR_Parm as parms
import tkinter as tk
from control_window import Control_Window
from timer_window import Timer_Window
from obs_xface import OBS_Xface, OBS_Error

from time import sleep

class Story_Room():

    def __init__(self):
        self._debug = True 

        self.state = Recording_State.INIT
        self.wm = tk.Tk()
        self.cw = Control_Window(self.wm, parms, self.session_init, self.session_stop, self.debug_exit, debug=self._debug)
        self.tw = Timer_Window(self.wm)
        self.tw.set_txt(parms.timer_waiting_message)
        self.obs = OBS_Xface(host='localhost', port=4444,password='family',callback=self.on_obs_event)
        self.cw.set_infoline(parms.info_line.format(version, self.obs.obs_version, self.obs.ws_version), parms.text_soft_color)

        self.show_disk_space()

        self.session_reset()

        self.wm.withdraw() # hide the toplevel window
        self.wm.mainloop() # handle window events

    def session_init(self):
        self.state = Recording_State.COUNTDOWN
        self.cw.disable_start_button()
        # TODO: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the non-C: drive)
        # TODO: get the desired filename
        self.cw.enable_stop_button()
        self.tw.start_countdown('Start recording in {} seconds', 10, 1, 5, 0, self.session_start_recording)

    def session_start_recording( self ):
        self.state = Recording_State.RECORDING
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.obs.start_recording()
        self.tw.start_countdown('Recording time remaining: {} minutes', 120, 60, 90, 60, self.session_end_warn)

    def session_end_warn(self):
        self.tw.start_countdown('Recording time remaining: {} seconds', 60, 1, 60, 0, self.session_end_recording)

    def session_end_recording(self):
        self.cw.disable_stop_button()
        self.obs.stop_recording()
        self.state = Recording_State.FINISHING
        self.tw.set_txt('Recording Stopped')
        # TODO: copy to USB, 
        self.tw.set_txt('Copying to USB')
        if self._debug: sleep(3) # pretend to copy
        # TODO: save to archive
        self.session_reset()

    def session_stop(self): # early stop of recording
        if self.state == Recording_State.COUNTDOWN:
            self.tw.stop_countdown(self.session_reset)
        elif self.state == Recording_State.RECORDING:
            self.tw.stop_countdown(self.session_end_recording)
        self.state = Recording_State.ABORTING
        if self._debug: print('aborting')

    def session_reset(self): # reset environment for next recording
        if self._debug: print('session_reset')
        self.tw.set_txt(parms.timer_waiting_message)
        self.cw.disable_stop_button()
        self.cw.enable_start_button()
        self.state = Recording_State.READY

    def on_obs_event(self, desc):
        print(f'on_obs_event: {desc}')

    def show_disk_space(self):
        if self._debug: print(f'free: {self.obs.disk_space / 1024}, min:{parms.free_disk_min}')
        if self.obs.disk_space < parms.free_disk_min:
            self.cw.dsklabel.config( bg = parms.text_warn_color )
        else:
            self.cw.dsklabel.config( bg = parms.bg_color )
        self.cw.set_diskline(parms.disk_line.format(self.obs.disk_space / 1024), parms.text_soft_color)
        self.wm.after( parms.fd_delay, self.show_disk_space ) 

    def debug_exit(self, e):
        print(f'\n>>> debug exit initiated with {e}')
        if self.state == Recording_State.RECORDING:
            self.obs.stop_recording()
        self.wm.after_cancel(self.show_disk_space)        
        self.cw.destroy()
        self.tw.destroy()
        self.wm.destroy()
        print('windows destroyed')
        exit(255)

if __name__ == '__main__':
    st = Story_Room()
