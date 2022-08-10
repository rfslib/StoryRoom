'''
file: story_room.py
author: rfslib

control "Story Room" recording sessions
'''
# TODO: !!! drive eject needs a callback, since it doesn't always eject the first try, which means two different ones depending on at beginning or after copy
# TODO: USB disconnect (after os.sync)
# TODO: stop showing USB info when it isn't attached (huh?)
# TODO: force focus on control_window
# TODO: all logic needs review after moving countdown stuff from timer_window
# TODO: prompt to remove drive if already inserted on startup (prompts for name twice as well :p)
# TODO: verify space on USB drive
# TODO: verify space on system drive(s)
# TODO: copy overwrite destination: verify it doesn't exist or add date and time to output filename
# TODO: check that OBS is running and start it before starting countdown to recording start
# TODO: periodically check OBS status (every nn seconds)
# TODO: check event against expected action and status
# TODO: consider OBS portable mode (config settings are saved in the OBS main folder) see obsproject.com/forum/resources/obs-and-obs-studio-portable-mode-on-windows.359
# TODO: OBS Event: 'SourceDestroyed', Raw data: {'sourceKind': 'scene', 'sourceName': 'Scene', 'sourceType': 'scene', 'update-type': 'SourceDestroyed'}: close app
# TODO: capture OS events (i.e., close app, etc.)
# TODO: catch OBS events (? under what conditions? connect() has to be active)
# TODO: installer (installation instructions)
# TODO: (OBS) create sources, lock configuration files
# TODO: check, set Sources, Profile, Scene (create standards for these)
# TODO: set filename format (SetFilenameFormatting)
# TODO: QSG (have this app set all parameters so no manual settings are required)
# TODO: warn on version mismatch for OBS, websockets and simpleobsws
# CAN: NO: change timer_window message when copy is complete
# DONE: don't show time left during lead-in countdown
# DONE: detect USB drive, copy file at end of recording
# DONE: get the desired filename
# DONE: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the non-C: drive)
# DONE: disable buttons when not valid
# DONE: finish logic to abort recording (countdown to start vs middle of recording)
# DONE: button/function to stop recording early
# DONE: change to seconds remaining on final 2 minutes of recording
# DONE: warn on low disk space (use psutil.disk_usage(".").free/1024/1024/1024)
# DONE: start OBS here or a separate class instead of startup so it can be checked/started from here

version = '20220725'

import tkinter as tk
#import psutil
from psutil import disk_partitions
from psutil import disk_usage

from os.path import basename
from os import system
from shutil import copy

from sr_parm import SR_Parm as cfg
from sr_parm import Recording_State
from control_window import Control_Window
from timer_window import Timer_Window
from obs_xface import OBS_Xface, OBS_Error
from get_kb_text import get_kb_text

class Story_Room():

    _debug = False

    state = Recording_State.INIT 
    usb_drive = ''
    usb_drive_mounted = False
    output_file_name = ''

    ## countdown stuff, set in start_countdown()
    tw_countdown_seconds = 10
    tw_countdown_active = False
    tw_countdown_complete = False
    tw_countdown_interval = 1
    tw_countdown_warn = 5
    tw_countdown_return = 0 # non-zero value means exec callback at n seconds
    tw_countdown_string = '{} seconds remaining'
    tw_countdown_abort = False
    tw_show_cw_timer = True

    def __init__(self):
        
        self.wm = tk.Tk()
        self.cw = Control_Window(self.wm, self.session_init, self.session_stop, self.debug_exit, debug=self._debug)
        self.update_state(Recording_State.INIT)
        self.tw = Timer_Window(self.wm)
        self.kb = get_kb_text(self.wm)

        self.usb_status_updater = None
        
        self.obs1 = OBS_Xface(host=cfg.obs1_host, port=cfg.obs1_port, password=cfg.obs1_pswd, callback=self.on_obs1_event)
        if self._debug: print(f'>>> obs1 configured: {self.obs1}')
        if cfg.obs2_host != '':
            self.obs2 = OBS_Xface(host=cfg.obs2_host, port=cfg.obs2_port, password=cfg.obs2_pswd, callback=self.on_obs2_event)
            if self._debug: print(f'>>> obs2 configured: {self.obs2}')
        self.update_obs_status()

        self.set_usb_drive()
        self.update_usb_drive_status()
        if self._debug: print(f'>>> init: drive: "{self.usb_drive}"')
        if self.usb_drive != '':
            self.update_state(Recording_State.DRIVE_ALREADY)
            self.eject_drive()
        self.wait_for_drive_removal() # starts the process

        self.wm.withdraw() # hide the toplevel window
        self.wm.mainloop() # handle window events
### --- end of init

### --- start of usb drive stuff
    def set_usb_drive(self): # assumes that the first removable drive is the one to write the video to
        # NOTE: when the drive is inserted AND mounted, the fstype shows (i.e. 'FAT32') and opts contains 'rw,removable';
        #       when the drive is 'ejected' but not removed, it maintains the drive letter, but fstype is an empty string and opts contains just 'removable'
        #       when the drive is removed, it no longer has an entry in disk_partitions()
        self.usb_drive_mounted = False
        self.usb_drive = ''
        disk_info = disk_partitions()
        for drive in disk_info:
            if 'removable' in drive.opts.lower():
                self.usb_drive = drive.mountpoint[0] # get just the letter
                if drive.fstype != '':
                    self.usb_drive_mounted = True
                print(f'>>> set_usb_drive: {drive.mountpoint} {drive.opts:16s} {drive.fstype:8s}')
                break

    def eject_drive(self):
        if self._debug: print(f'>>> eject_drive "{self.usb_drive}"')
        self.set_usb_drive()
        if self.usb_drive != '':
            if self.usb_drive_mounted == True:
                # the following line from https://stackoverflow.com/questions/70051578/eject-deivce-usb-using-python-e-windows-10/
                self.usb_drive_mounted = False # assume that the eject will actually work
                eject_line = f'powershell $driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).parseName("""{self.usb_drive}:""").InvokeVerb("""Eject""")'
                if self._debug: print(f'>>> sending {eject_line}')
                system(eject_line) # 'eject' the usb drive
                if self._debug: print(f'>>> eject statement executed: usb_drive: {self.usb_drive}, mounted: {self.usb_drive_mounted}')
                self.wm.after(1000, self.eject_drive)

    def wait_for_drive_removal(self): # wait for the USB drive to be removed
        if self._debug: print('>>> wait_for_drive_removal')
        self.set_usb_drive()
        if self.usb_drive != '':
            self.wm.after(1000, self.wait_for_drive_removal)
        else:
            self.session_reset()

    def wait_for_drive(self): # wait for a USB drive to be plugged in to get the session going
        self.set_usb_drive()
        if self.usb_drive != '' and self.usb_drive_mounted == True:
            self.update_state(Recording_State.DRIVE_INSERTED)
            if self._debug: print(f'>>> usb drive is on {self.usb_drive}:')
            self.session_get_filename()
        else:
            self.wm.after(1000, self.wait_for_drive)

    def update_usb_drive_status(self):
        # update ubs drive status if present
        text_color=cfg.c_text_info_color
        if self.usb_drive != '' and self.usb_drive_mounted == True:
            try:
                usb_free_disk = disk_usage('{}:\\'.format(self.usb_drive)).free / 1024 / 1024 / 1024                
                self.cw.set_info_line_3(cfg.info_line.format('USB Drive', 'available', usb_free_disk), text_color)
            except:
                self.cw.set_info_line_3('---', text_color)
        else:
            self.cw.set_info_line_3('', text_color)
        # re-run ourself in a few seconds
        self.usb_status_updater = self.wm.after(cfg.fd_delay, self.update_usb_drive_status) 
### --- end drive stuff

### --- start of session control stuff
    def session_get_filename(self):
        self.update_state(Recording_State.GET_FILENAME)
        self.output_file_name = self.kb.get_text('Enter filename: ')
        ### NOTE: if output_file_name is left an empty string, it will use basename in session_end_recording() 
        if self._debug: print(f'>>> session_get_filename: {self.output_file_name}')
        self.update_state(Recording_State.WAIT_FOR_START)
        self.cw.enable_start_button()

    def session_init(self):
        self.update_state(Recording_State.COUNTDOWN)
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.start_countdown(msg_text=cfg.t_leadin_msg, length=cfg.t_leadin_to_start, 
            upd_every=1, warn_at=cfg.t_leadin_warn_at, return_at=0, show_cw_timer=False, callback=self.session_start_recording)

    def session_start_recording( self ):
        self.update_state(Recording_State.RECORDING)
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.obs1.start_recording()
        if cfg.obs2_host != '':
            self.obs2.start_recording()
        self.start_countdown(msg_text=cfg.t_record_msg, length=cfg.t_record_length,
            upd_every=cfg.t_record_interval, warn_at=cfg.t_record_warn_at, return_at=cfg.t_record_return_at, show_cw_timer=True, callback=self.session_end_warn)

    def session_end_warn(self):
        self.start_countdown(msg_text=cfg.t_end_msg, length=cfg.t_record_return_at, 
            upd_every=cfg.t_end_interval, warn_at=cfg.t_record_return_at, return_at=0, show_cw_timer=True, callback=self.session_end_recording)

    def session_stop(self): # early stop of recording
        self.cw.disable_stop_button()
        if self._debug: print('aborting')
        if self.state == Recording_State.COUNTDOWN:
            self.update_state(Recording_State.ABORTING)
            self.stop_countdown(self.session_reset)
        elif self.state == Recording_State.RECORDING:
            self.update_state(Recording_State.ABORTING)
            self.stop_countdown(self.session_end_recording)

    def session_end_recording(self): # stop recording and copy to USB, then prompt to remove drive
        # stop the recording
        self.update_state(Recording_State.FINISHING)
        self.cw.disable_stop_button()
        self.cw.set_time_left('', cfg.c_text_soft_color)
        self.obs1.stop_recording()
        if cfg.obs2_host != '':
            self.obs2.stop_recording()
        self.tw.set_txt('Recording Stopped')
        # build the output filename and copy
        if self.output_file_name == '': # if no file name given, use default from OBS
            self.output_file_name = basename(self.obs1.file_name)
        else:
            self.output_file_name += '.mkv'
        dest_filename = '{}:\\{}'.format(self.usb_drive, self.output_file_name)
        if self._debug: print(f'>>> copying {self.obs1.file_name} to {dest_filename}') 
        self.update_state(Recording_State.COPYING)
        self.tw.set_txt('Copying the video to the USB drive...')
        copy(self.obs1.file_name, dest_filename)
        self.eject_drive()
        self.update_state(Recording_State.DRIVE_READY)
        self.wait_for_drive_removal()
  
    def session_reset(self): # reset environment for next recording
        self.update_state(Recording_State.FINISHED)
        if self._debug: print('session_reset')
        self.tw.set_txt(cfg.timer_waiting_message)
        self.cw.disable_stop_button()
        self.cw.disable_start_button()
        self.usb_drive = ''
        self.update_state(Recording_State.WAIT_FOR_DRIVE)
        self.wait_for_drive() # wait for next USB drive to start next session
### --- end of session control stuff

### --- start of status update stuff and event handlers
    def update_state(self, state_now: Recording_State):
        self.state = state_now
        self.cw.set_state_line(self.state.value, cfg.c_state_font_color)
        self.cw.update()

    def on_obs1_event(self, desc):
        print(f'>>> on_obs1_event: {desc}')

    def on_obs2_event(self, desc):
        print(f'>>> on_obs2_event: {desc}')

    def update_obs_status(self):
        if self._debug: print('>>> update_sys_lines: ')
        # update main recording system status
        if self.obs1.disk_space < cfg.free_disk_min:
            text_color=cfg.c_text_warn_color
        else:
            text_color=cfg.c_text_info_color
        self.cw.set_info_line_1(cfg.info_line.format('Main System', self.obs1.obs_status, self.obs1.disk_space/1024 ), text_color) 
        # update backup recording system status if configured
        if cfg.obs2_host == '':
            self.cw.set_info_line_2('Backup system not configured', cfg.c_text_info_color)
        else:
            if self.obs2.disk_space < cfg.free_disk_min:
                text_color=cfg.c_text_warn_color
            else:
                text_color=cfg.c_text_info_color
            self.cw.set_info_line_2(cfg.info_line.format('Backup System', self.obs2.obs_status, self.obs2.disk_space/1024 ), text_color) 
        # re-run ourself in a few seconds
        self.obs_status_updater = self.wm.after(cfg.fd_delay, self.update_obs_status) 
### --- end of status update and background tasks

### --- timer stuff
    def start_countdown(self, msg_text:str='countdown: {}', length:int=20, upd_every: int=1, warn_at: int=10, return_at: int=0, show_cw_timer: int=True, callback=None):
        if self.tw_countdown_active: return -1 # a countdown is already active, can't start another
        self.tw_countdown_active = True # set "in-countdown" flag
        if self._debug: print(f'>>> start_countdown: count down {length} seconds, update every {upd_every} seconds')
        self.tw_countdown_string = msg_text
        self.countdown_callback = callback
        self.tw_countdown_seconds = length
        self.tw_countdown_interval = upd_every
        self.tw_countdown_warn = warn_at
        self.tw_countdown_return = return_at
        self.tw_countdown_complete = False
        self.tw_countdown_abort = False
        self.tw_show_cw_timer = show_cw_timer
        self.tw.set_alpha(cfg.tw_normalpha)
        self.tw.set_bg(cfg.tw_normbg)
        self.countdown()  # start the countdown

    def stop_countdown(self, new_callback): # tell the current countdown to stop early
        self.countdown_callback = new_callback
        self.tw_countdown_abort = True

    def countdown(self):
        if self.tw_countdown_abort: # early stop flag set
            self.tw.set_txt('Stopped')
            if self._debug: print('>>> countdown: aborted')
            self.tw.set_alpha(cfg.tw_normalpha)
            self.tw.set_bg(cfg.tw_normbg)
            self.tw.set_label_bg(cfg.tw_normbg)
            self.tw_countdown_complete = True
            self.tw_countdown_active = False # clear in-countdown flag
            if self.countdown_callback != None: self.countdown_callback()
        elif self.tw_countdown_seconds > self.tw_countdown_return: # still time left
            if self.tw_countdown_seconds <= self.tw_countdown_warn:
                self.tw.set_alpha(cfg.tw_warnalpha)
                self.tw.set_bg(cfg.tw_warnbg)
                self.tw.set_label_bg(cfg.tw_warnbg)
            if not (self.tw_countdown_seconds % self.tw_countdown_interval): # update at every 'interval'
                self.tw.set_txt(self.tw_countdown_string.format(int(self.tw_countdown_seconds / self.tw_countdown_interval)))
                if self._debug: print(f'>>> countdown: at {self.tw_countdown_seconds} seconds')
                if self.tw_show_cw_timer:
                    if self.tw_countdown_seconds < 60:
                        self.cw.set_time_left('<1 minute', cfg.c_text_info_color)
                    else:
                        self.cw.set_time_left(cfg.c_time_left_msg.format(int(self.tw_countdown_seconds / 60)), cfg.c_text_info_color)
            self.tw_countdown_seconds -= 1
            self.wm.after(int(cfg.t_drift * 1000), self.countdown)
        else: # time is up
            self.tw.set_txt('')
            self.cw.set_time_left('', cfg.c_text_soft_color)
            if self._debug: print( '>>> countdown: complete')
            self.tw.set_alpha(cfg.tw_normalpha)
            self.tw.set_bg(cfg.tw_normbg)
            self.tw.set_label_bg(cfg.tw_normbg)
            self.tw_countdown_complete = True
            self.tw_countdown_active = False # clear in-countdown flag
            if self.countdown_callback != None: self.countdown_callback()
### --- end timer stuff

### --- miscellaneous
    def debug_exit(self, e):
        self.cw.withdraw()     
        try: self.wm.after_cancel(self.obs_status_updater)
        except: pass
        try: self.wm.after_cancel(self.usb_status_updater)
        except: pass
        self.cw.set_state_line(f'\n>>> debug_exit: initiated with {e}', cfg.c_state_font_color)
        if self._debug: print(f'\n>>> debug_exit: initiated with {e}')
        self.tw.destroy()   
        self.kb.destroy()    
        if self.state == Recording_State.RECORDING:
            self.obs1.stop_recording()
            if cfg.obs2_host != '':
                self.obs2.stop_recording()
        try: self.obs1.__del__()
        except: pass
        if cfg.obs2_host != '':
            self.obs2.__del__()  
        self.cw.destroy()
        self.wm.destroy()
        exit(17)
### --- end miscellaneous

### --- main
if __name__ == '__main__':
    st = Story_Room()
    st.wait_for_drive() # drive insertion starts a recording session
