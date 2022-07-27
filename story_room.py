'''
file: story_room.py
author: rfslib

control "Story Room" recording sessions
'''
# TODO: USB disconnect
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
# DONE: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the non-C: drive)
# DONE: disable buttons when not valid
# DONE: finish logic to abort recording (countdown to start vs middle of recording)
# DONE: button/function to stop recording early
# DONE: change to seconds remaining on final 2 minutes of recording
# DONE: warn on low disk space (use psutil.disk_usage(".").free/1024/1024/1024)
# DONE: start OBS here or a separate class instead of startup so it can be checked/started from here

version = '20220725'


'''
A class for the current program state
'''
from enum import Enum, auto

class Recording_State(Enum):
    INIT = auto()           # program initialization
    WAIT_FOR_DRIVE = auto() # ready to record
    DRIVE_INSERTED = auto() # a removable drive has been connected
    GET_FILENAME = auto()   # get the final filename
    WAIT_FOR_START = auto() # ready to record, waiting for go to start countdown
    COUNTDOWN = auto()      # countdown to start of recording is in progress
    RECORDING = auto()      # recording is in progress
    ABORTING = auto()       # early stop of recording was requested
    FINISHING = auto()      # recording stop has been requested
    FINISHED = auto()       # recording has stopped (reMUX in progress)
    COPYING = auto()        # video file is being copied to removable drive
    DRIVE_READY = auto()    # copy is complete, waiting for drive to be removed
    DRIVE_REMOVED = auto()  # drive removed
    CLEANUP = auto()        # cleanup in progress: extra files being removed, session being reset


import tkinter as tk
from time import sleep
import psutil
from os.path import basename
from shutil import copy

from sr_parm import SR_Parm as cfg
from control_window import Control_Window
from timer_window import Timer_Window
from obs_xface import OBS_Xface, OBS_Error
from get_kb_text import get_kb_text

class Story_Room():

    def __init__(self):
        
        self._debug = True 

        self.state = Recording_State.INIT
        self.usb_drive = ''
        self.output_file_name = ''

        self.wm = tk.Tk()
        self.cw = Control_Window(self.wm, self.session_init, self.session_stop, self.debug_exit, debug=self._debug)
        self.tw = Timer_Window(self.wm)
        #self.kb = get_kb_text(self.wm)
        self.update_state()
        
        self.obs1 = OBS_Xface(host=cfg.obs1_host, port=cfg.obs1_port, password=cfg.obs1_pswd, callback=self.on_obs1_event)
        if cfg.obs2_host != '':
            self.obs2 = OBS_Xface(host=cfg.obs2_host, port=cfg.obs2_port, password=cfg.obs2_pswd, callback=self.on_obs2_event)
        self.update_sys_lines()

        self.session_reset()
        self.wait_for_drive()

        self.wm.withdraw() # hide the toplevel window
        self.wm.mainloop() # handle window events

    def wait_for_drive(self): # wait for a USB drive to be plugged in to get the session going
        drives = self.get_drives()
        if len(drives) > 0:
            self.state = Recording_State.DRIVE_INSERTED
            self.usb_drive = drives[0]
            if self._debug: print(f'>>> usb drive is on {self.usb_drive}:')
            self.session_get_filename()
        else:
            self.wm.after(1000, self.wait_for_drive)

    def session_get_filename(self):
        # TODO: get filename and get things ready to record
        self.state = Recording_State.GET_FILENAME
        self.output_file_name = 'foo.mkv'
        print(f'>>> get_filename: {self.output_file_name}')
        self.state = Recording_State.WAIT_FOR_START
        self.cw.enable_start_button()

    def session_init(self):
        self.state = Recording_State.COUNTDOWN
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.tw.start_countdown('Start recording in {} seconds', 10, 1, 5, 0, self.session_start_recording)

    def session_start_recording( self ):
        self.state = Recording_State.RECORDING
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.obs1.start_recording()
        self.tw.start_countdown('Recording time remaining: {} minutes', 120, 60, 90, 60, self.session_end_warn)

    def session_end_warn(self):
        self.tw.start_countdown('Recording time remaining: {} seconds', 60, 1, 60, 0, self.session_end_recording)

    def session_end_recording(self):
        self.cw.disable_stop_button()
        self.obs1.stop_recording()
        self.tw.set_txt('Recording Stopped')
        self.state = Recording_State.COPYING
        dest_file = '{}:\\{}'.format(self.usb_drive, self.output_file_name)
        if self._debug: print(f'>>> copying {self.obs1.file_name} to {dest_file}')
        # TODO: copy to USB, 
        #self.tw.set_txt('Copying to USB')
        copy(self.obs1.file_name, dest_file)
        if self._debug: sleep(5) # pretend to copy
        # TODO: save to archive
        self.session_reset()

    def session_stop(self): # early stop of recording
        if self._debug: print('aborting')
        if self.state == Recording_State.COUNTDOWN:
            self.state = Recording_State.ABORTING
            self.tw.stop_countdown(self.session_reset)
        elif self.state == Recording_State.RECORDING:
            self.state = Recording_State.ABORTING
            self.tw.stop_countdown(self.session_end_recording)
        
    def session_reset(self): # reset environment for next recording
        self.state = Recording_State.FINISHING
        if self._debug: print('session_reset')
        self.tw.set_txt(cfg.timer_waiting_message)
        self.cw.disable_stop_button()
        self.cw.disable_start_button()
        self.usb_drive = ''
        self.state = Recording_State.WAIT_FOR_DRIVE


    def update_state(self):
        msg = ''
        clr=cfg.state_font_color
        if self.state == Recording_State.INIT:
            msg = 'Initializing the system'
        elif self.state == Recording_State.WAIT_FOR_DRIVE:
            msg = 'System Ready. Insert a new USB drive to begin...'
            self.tw.set_txt(cfg.timer_waiting_message)
        elif self.state == Recording_State.DRIVE_INSERTED:
            msg = 'Drive attached.'
            self.tw.set_txt('Drive attached.')
        elif self.state == Recording_State.GET_FILENAME:
            msg = 'Enter a name for the video file...'
        elif self.state == Recording_State.WAIT_FOR_START:
            msg = 'Everything is ready. Tap the "Start Recording" button to begin...'
        elif self.state == Recording_State.COUNTDOWN:
            msg = 'Counting down to start of recording. You can leave the room now :)'
        elif self.state == Recording_State.RECORDING:
            msg = 'Recording. Please wait for the recording time to expire (or press the stop button to end it early).'
        elif self.state == Recording_State.ABORTING:
            msg = 'Early stop of the recording requested. Stopping the Recording.'
        elif self.state == Recording_State.FINISHING:
            msg = 'Recording has stopped. Re-muxing the file and preparing to copy to the USB drive.'
        elif self.state == Recording_State.COPYING:
            msg = 'Copying the video file to the USB drive. Please wait...'
            self.tw.set_txt('Copying video to USB drive...')
        elif self.state == Recording_State.DRIVE_READY:
            msg = 'Copy to the USB drive is complete. Please remove the drive now...'
            self.tw.set_txt('USB drive is ready to remove')
        elif self.state == Recording_State.DRIVE_REMOVED:
            msg = 'USB Drive removed. Bringing out the janitorial supplies.'
        elif self.state == Recording_State.CLEANUP:
            msg = 'Recording session is over. Preparing the system for the next session.'
        else:
            msg = 'UNKNOWN STATE: something is broken!'
        self.cw.set_state_line(msg, clr)
        self.cw.update()
        self.wm.after(1000, self.update_state)

    def on_obs1_event(self, desc):
        print(f'on_obs1_event: {desc}')

    def on_obs2_event(self, desc):
        print(f'on_obs2_event: {desc}')

    def update_sys_lines(self):
        if self._debug: print('>>> update_sys_lines')
        if self.obs1.disk_space < cfg.free_disk_min:
            text_color=cfg.text_warn_color
        else:
            text_color=cfg.text_info_color
        self.cw.set_info_line_1(cfg.info_line.format('Main', self.obs1.obs_status, self.obs1.disk_space/1024 ), text_color) 

        if cfg.obs2_host == '':
            self.cw.set_info_line_2('Backup system not configured', cfg.text_info_color)
        else:
            if self.obs2.disk_space < cfg.free_disk_min:
                text_color=cfg.text_warn_color
            else:
                text_color=cfg.text_info_color
            self.cw.set_info_line_2(cfg.info_line.format('Backup', self.obs2.obs_status, self.obs2.disk_space/1024 ), text_color) 

        self.wm.after(cfg.fd_delay, self.update_sys_lines) 

    def get_drives(self): # return a list of current drives
        drive_list = []
        disk_info = psutil.disk_partitions()
        for drive in disk_info:
            if 'removable' in drive.opts.lower():
                drive_list.append(drive.mountpoint[0])
        return drive_list

    def debug_exit(self, e):
        print(f'\n>>> debug exit initiated with {e}')
        if self.state == Recording_State.RECORDING:
            self.obs1.stop_recording()
        self.wm.after_cancel(self.update_sys_lines)        
        self.wm.after_cancel(self.update_state)        
        self.cw.destroy()
        self.tw.destroy()
        self.wm.destroy()
        print('windows destroyed')
        exit(255)

if __name__ == '__main__':
    st = Story_Room()
    st.wait_for_drive() # drive insertion starts a recording session
