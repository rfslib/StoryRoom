'''
file: story_room.py
author: rfslib

control "Story Room" recording sessions
'''
# TODO: cancel on countdown needs to return to drive removal
# TODO: force focus on control_window
# TODO: all logic needs review after moving countdown stuff from timer_window
# TODO: verify space on USB drive
# TODO: verify space on system drive(s)
# TODO: check that OBS is running and start it before starting countdown to recording start
# TODO: check event against expected action and status
# TODO: consider OBS portable mode (config settings are saved in the OBS main folder) see obsproject.com/forum/resources/obs-and-obs-studio-portable-mode-on-windows.359
# TODO: OBS Event: 'SourceDestroyed', Raw data: {'sourceKind': 'scene', 'sourceName': 'Scene', 'sourceType': 'scene', 'update-type': 'SourceDestroyed'}: close app
# TODO: capture OS events (i.e., close app, etc.)
# TODO: installer (installation instructions)
# TODO: (OBS) create sources, lock configuration files
# TODO: check, set Sources, Profile, Scene (create standards for these)
# TODO: set filename format (SetFilenameFormatting)
# TODO: QSG (have this app set all parameters so no manual settings are required)
# TODO: warn on version mismatch for OBS, websockets and simpleobsws
# DONE: periodically check OBS status (every nn seconds)
# DONE: catch OBS events (? under what conditions? connect() has to be active)
# DONE: copy overwrite destination prevention: add date and time to output filename (%CCYY-%MM-%DD_%hh-%mm-%ss -> %Y-%m-%d_%H:%M:%S)
# DONE: prompt to remove drive if already inserted on startup (prompts for name twice as well :p)
# DONE: !!! drive eject needs a callback, since it doesn't always eject the first try, which means two different ones depending on at beginning or after copy
# DONE: USB disconnect (after os.sync)
# DONE: stop showing USB info when it isn't attached (huh?)
# CANCEL: NO: change timer_window message when copy is complete
# DONE: don't show time left during lead-in countdown
# DONE: detect USB drive, copy file at end of recording
# DONE: get the desired filename
# DONE: detect USB drive and available space (NOTE: only one USB port will be physically exposed, so this will be the only removable drive)
# DONE: disable buttons when not valid
# DONE: finish logic to abort recording (countdown to start vs middle of recording)
# DONE: button/function to stop recording early
# DONE: change to seconds remaining on final 2 minutes of recording
# DONE: warn on low disk space (use psutil.disk_usage(".").free/1024/1024/1024)
# DONE: start OBS here or a separate class instead of startup so it can be checked/started from here

version = '20220818'

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
        
        self.wm = tk.Tk() # the toplevel Tk window (not shown)
        self.wm.withdraw() # hide the toplevel window

        
        # set up the control screen
        self.cw = Control_Window(self.wm, self.session_init, self.session_stop, self.debug_exit, debug=self._debug)
        self.update_state(Recording_State.INIT)

        # set up the timer display on the video monitor (OBS calls it a 'projector')
        self.tw = Timer_Window(self.wm)

        # set up the keyboard entry window (for getting a filename)
        self.kb = get_kb_text(self.wm)

        # open a channel (websocket) to OBS on this system and on a remote backup system
        self.obs1 = OBS_Xface(host=cfg.obs1_host, port=cfg.obs1_port, password=cfg.obs1_pswd, callback=self.on_obs1_event)
        if self._debug: print(f'>>> obs1 configured: {self.obs1}')
        if cfg.obs2_host != '': # if a backup system is configured, connect to it
            try:
                self.obs2 = OBS_Xface(host=cfg.obs2_host, port=cfg.obs2_port, password=cfg.obs2_pswd, callback=self.on_obs2_event)
            except:
                self.obs2 = None
                print('>>> Backup OBS did not respond!!!')
            if self._debug: print(f'>>> obs2 configured: {self.obs2}')

        # start the OBS status updater; since this will run forever, 
        self.obs_status_updater = None # holds the update method 'after' call so it can be stopped on exit
        self.update_obs_status() # start the updater, which keeps itself going with an 'after' call

        # start the USB status updater
        self.usb_status_updater = None # a place to hold the USB status line update method 'after' call so it can be stopped on exit
        self.set_usb_drive() # set the current
        self.update_usb_drive_status() # start the status updater, which keeps itself going with and 'after' call

        if self._debug: print(f'>>> init: drive: "{self.usb_drive}"')
        if self.usb_drive != '':
            self.update_state(Recording_State.DRIVE_ALREADY)
            self.eject_drive()
        self.wait_for_drive_removal() # starts the process
        
        self.wm.mainloop() # handle window events
### --- end of init


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
        if self.obs2 != None: # cfg.obs2_host != '':
            try:
                self.obs2.start_recording()
            except:
                print('>>> obs2 has stopped responsding: can\'t start recording')
                self.obs2 = None
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
        if self.obs2 != None: # cfg.obs2_host != '':
            try:
                self.obs2.stop_recording()
            except:
                print('>>> obs2 has stopped responding: can\'t stop recording')
                self.obs2 = None
        self.tw.set_txt('Recording Stopped')
        # build the output filename and copy
        if self.output_file_name == '': # if no file name given, use default from OBS
            self.output_file_name = basename(self.obs1.file_name) # default name is date/time
        else:
            self.output_file_name += '_' + basename(self.obs1.file_name) # add date/time to chosen name to avoid conflicts (multi-session recordings)
        dest_filename = '{}:\\{}'.format(self.usb_drive, self.output_file_name) # prepend the USB drive letter
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
        self.cw.set_event_line_1('')
        self.cw.set_event_line_2('')
        self.update_state(Recording_State.WAIT_FOR_DRIVE)
        self.wait_for_drive() # wait for next USB drive to start next session
### --- end of session control stuff

### --- start of usb drive stuff
    def set_usb_drive(self): # assumes that the first removable drive is the one to write the video to
        # NOTE: when the drive is inserted AND mounted, the fstype isn't an emptry string (i.e. 'FAT32') and opts contains 'rw,removable';
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
                if self._debug: print(f'>>> set_usb_drive: {drive.mountpoint} {drive.opts:16s} {drive.fstype:8s}')
                break

    def eject_drive(self):
        if self._debug: print(f'>>> eject_drive "{self.usb_drive}"')
        self.set_usb_drive()
        if self.usb_drive != '':
            if self.usb_drive_mounted == True:
                # the following line from https://stackoverflow.com/questions/70051578/eject-deivce-usb-using-python-3-windows-10/
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
        if self.usb_drive != '':
            if self.usb_drive_mounted:
                try:
                    usb_free_disk = disk_usage('{}:\\'.format(self.usb_drive)).free / 1024 / 1024 / 1024                
                    self.cw.set_info_line_3(cfg.info_line.format('USB Drive', 'available', usb_free_disk), text_color)
                except:
                    self.cw.set_info_line_3('Could not read USB drive', text_color)
            else:
                self.cw.set_info_line_3(cfg.c_usb_remove_msg, text_color)
        else:
            self.cw.set_info_line_3('', text_color)
        # re-run ourself in a few seconds
        self.usb_status_updater = self.wm.after(cfg.update_usb_status_delay, self.update_usb_drive_status) 
### --- end usb drive stuff


### --- start of status update stuff and event handlers
    def update_state(self, state_now: Recording_State):
        self.state = state_now
        self.cw.set_state_line(self.state.value, cfg.c_state_font_color)
        self.cw.update()

    def on_obs1_event(self, desc):
        print(f'>>> on_obs1_event: {desc}')
        self.cw.set_event_line_1('obs 1: {}'.format(desc['update-type']))

    def on_obs2_event(self, desc):
        print(f'>>> on_obs2_event: {desc}')
        self.cw.set_event_line_2('obs 2: {}'.format(desc['update-type']))

    def update_obs_status(self):
        if self._debug: print('>>> update_obs_status: ')
        # update main recording system status
        self.obs1.get_obs_stats()
        if self.obs1.disk_space < cfg.free_disk_min:
            text_color=cfg.c_text_warn_color
        else:
            text_color=cfg.c_text_info_color
        self.cw.set_info_line_1(cfg.info_line.format(cfg.c_main_system_name, self.obs1.obs_status, self.obs1.disk_space/1024 ), text_color) 
        # update backup recording system status if configured            
        if self.obs2 != None:
            try:
                self.obs2.get_obs_stats()
                if self.obs2.disk_space < cfg.free_disk_min:
                    text_color=cfg.c_text_warn_color
                else:
                    text_color=cfg.c_text_info_color
                self.cw.set_info_line_2(cfg.info_line.format(cfg.c_backup_system_name, self.obs2.obs_status, self.obs2.disk_space/1024 ), text_color) 
            except:
                print('>>> obs2 has stopped responding: can\'t update status')
                self.obs2 = None
                self.cw.set_info_line_2(cfg.c_backup_unavailable_msg, cfg.c_text_warn_color)         
        else:
            self.cw.set_info_line_2(cfg.c_backup_unavailable_msg, cfg.c_text_warn_color)
        # re-run ourself after the configured time
        self.obs_status_updater = self.wm.after(cfg.update_obs_status_delay, self.update_obs_status) 
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
        #self.kb.__del__() # 
        self.kb.destroy()    
        if self.state == Recording_State.RECORDING:
            try:
                self.obs1.stop_recording()
                if self.obs2 != None: # cfg.obs2_host != '':
                    self.obs2.stop_recording()
            except:
                pass
        try: self.obs1.__del__()
        except: pass
        if self.obs2 != None: # cfg.obs2_host != '':
            try: self.obs2.__del__()  
            except: pass
        self.cw.destroy()
        self.wm.destroy()
        exit(17)
### --- end miscellaneous

### --- main
if __name__ == '__main__':
    st = Story_Room()
    st.wait_for_drive() # drive insertion starts a recording session


    '''    
    self.action_complete = tk.BooleanVar()  # used to indicate when a self-calling method is complete

    def session_start(self):
        
        #    20220818: 
        #        while session control is currently all event-driven, it becomes a challenge to follow...
        #        so, this is an attempt to make this thing easier to follow (and maintain)
        while True:
            # if we're trying to start a new session and there's a usb drive in, get it removed
            self.set_usb_drive() # set the current
            if self.usb_drive != '':
                self.update_state(Recording_State.DRIVE_ALREADY)
                self.eject_drive()
            self.action_complete.set(False)
            self.wait_for_drive_removal() # starts the process
            self.wm.wait_variable(self.action_complete)

            # initialize session variables
            self.update_state(Recording_State.CLEANUP)
            self.tw.set_txt(cfg.timer_waiting_message)
            self.cw.disable_stop_button()
            self.cw.disable_start_button()
            self.cw.set_event_line_1('')
            self.cw.set_event_line_2('')

            # prompt and wait for a USB drive to be inserted
            self.update_state(Recording_State.WAIT_FOR_DRIVE)
            self.action_complete.set(False)
            self.session_wait_for_drive()
            self.wm.wait_variable(self.action_complete)

            # prompt for a filename for the video
            self.update_state(Recording_State.GET_FILENAME)
            self.output_file_name = self.kb.get_text('Enter filename: ')

            # prompt and wait for the start button to start
            self.update_state(Recording_State.WAIT_FOR_START)
            self.cw.enable_start_button()


            # start countdown for video start
            self.update_state(Recording_State.)

            # start recording and verify start
            self.update_state(Recording_State.)

            # wait for countdown to finish or keypress (to end recording early)
            self.update_state(Recording_State.)

            # stop recording
            self.update_state(Recording_State.)

            # copy video to USB drive
            self.update_state(Recording_State.)

            # prompt and wait for drive to be removed
            self.update_state(Recording_State.)

        ## end while True

    def session_wait_for_drive_removal(self): # loop until the usb drive is pulled
        if self.usb_drive != '':
            self.wm.after(1000, self.session_wait_for_drive_removal)
        else:
            self.action_complete.set(True)

    def session_wait_for_drive(self): # wait for a USB drive to be plugged in to get the session going
        self.set_usb_drive()
        if self.usb_drive != '' and self.usb_drive_mounted == True:
            self.action_complete.set(True)
        else:
            self.wm.after(1000, self.session_wait_for_drive)
        
        '''
### *** ---