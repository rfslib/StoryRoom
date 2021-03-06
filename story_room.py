'''
file: story_room.py
author: rfslib

control "Story Room" recording sessions
'''
# TODO: USB disconnect (after os.sync)
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
from time import sleep
#import psutil
from psutil import disk_partitions
from psutil import disk_usage

from os.path import basename
from shutil import copy

from sr_parm import SR_Parm as cfg
from sr_parm import Recording_State
from control_window import Control_Window
from timer_window import Timer_Window
from obs_xface import OBS_Xface, OBS_Error
from get_kb_text import get_kb_text

class Story_Room():

    def __init__(self):
        
        self._debug = False 

        self.state = Recording_State.INIT
        self.usb_drive = ''
        self.output_file_name = ''

        self.wm = tk.Tk()
        self.cw = Control_Window(self.wm, self.session_init, self.session_stop, self.debug_exit, debug=self._debug)
        self.tw = Timer_Window(self.wm)
        self.kb = get_kb_text(self.wm)
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
        self.state = Recording_State.GET_FILENAME
        self.output_file_name = self.kb.get_text('Enter filename: ')
        ### NOTE: if output_file_name is left an empty string, it will use basename in session_end_recording() 
        if self._debug: print(f'>>> session_get_filename: {self.output_file_name}')
        self.state = Recording_State.WAIT_FOR_START
        self.cw.enable_start_button()

    def session_init(self):
        self.state = Recording_State.COUNTDOWN
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.tw.start_countdown(msg_text=cfg.t_leadin_msg, length=cfg.t_leadin_to_start, 
            upd_every=1, warn_at=cfg.t_leadin_warn_at, return_at=0, callback=self.session_start_recording)

    def session_start_recording( self ):
        self.state = Recording_State.RECORDING
        self.cw.disable_start_button()
        self.cw.enable_stop_button()
        self.obs1.start_recording()
        self.tw.start_countdown(msg_text=cfg.t_record_msg, length=cfg.t_record_length,
            upd_every=cfg.t_record_interval, warn_at=cfg.t_record_warn_at, return_at=cfg.t_record_return_at, callback=self.session_end_warn)

    def session_end_warn(self):
        self.tw.start_countdown(msg_text=cfg.t_end_msg, length=cfg.t_record_return_at, 
            upd_every=cfg.t_end_interval, warn_at=cfg.t_record_return_at, return_at=0, callback=self.session_end_recording)

    def session_stop(self): # early stop of recording
        if self._debug: print('aborting')
        if self.state == Recording_State.COUNTDOWN:
            self.state = Recording_State.ABORTING
            self.tw.stop_countdown(self.session_reset)
        elif self.state == Recording_State.RECORDING:
            self.state = Recording_State.ABORTING
            self.tw.stop_countdown(self.session_end_recording)

    def session_end_recording(self): # stop recording and copy to USB, then prompt to remove drive
        # stop the recording
        self.state = Recording_State.FINISHING
        self.cw.disable_stop_button()
        self.obs1.stop_recording()
        self.tw.set_txt('Recording Stopped')
        # build the output filename and copy
        if self.output_file_name == '': # if no file name given, use default from OBS
            self.output_file_name = basename(self.obs1.file_name)
        else:
            self.output_file_name += '.mkv'
        dest_filename = '{}:\\{}'.format(self.usb_drive, self.output_file_name)
        if self._debug: print(f'>>> copying {self.obs1.file_name} to {dest_filename}') 
        self.tw.set_txt('Copying video to USB')
        self.state = Recording_State.COPYING
        self.tw.set_txt('Copying the video to the USB drive...')
        copy(self.obs1.file_name, dest_filename)
        if self._debug: sleep(5) # lengthen copy time to verify prompts
        # clear variables, etc. for the next session
        self.state = Recording_State.DRIVE_READY
        self.wait_for_drive_removal()

    def wait_for_drive_removal(self):
        drives = self.get_drives()
        if len(drives) > 0:
            self.wm.after(1000, self.wait_for_drive_removal)
        else:
            self.session_reset()
  
    def session_reset(self): # reset environment for next recording
        self.state = Recording_State.FINISHING
        if self._debug: print('session_reset')
        self.tw.set_txt(cfg.timer_waiting_message)
        self.cw.disable_stop_button()
        self.cw.disable_start_button()
        self.usb_drive = ''
        self.state = Recording_State.WAIT_FOR_DRIVE
        self.wait_for_drive() # wait for next USB drive to start next session

    def update_state(self):
        self.cw.set_state_line(self.state.value, cfg.state_font_color)
        self.cw.update()
        self.wm.after(1000, self.update_state)

    def on_obs1_event(self, desc):
        print(f'on_obs1_event: {desc}')

    def on_obs2_event(self, desc):
        print(f'on_obs2_event: {desc}')

    def update_sys_lines(self):
        if self._debug: print('>>> update_sys_lines: ')
        if self.obs1.disk_space < cfg.free_disk_min:
            text_color=cfg.c_text_warn_color
        else:
            text_color=cfg.c_text_info_color
        self.cw.set_info_line_1(cfg.info_line.format('Main System', self.obs1.obs_status, self.obs1.disk_space/1024 ), text_color) 

        if cfg.obs2_host == '':
            self.cw.set_info_line_2('Backup system not configured', cfg.c_text_info_color)
        else:
            if self.obs2.disk_space < cfg.free_disk_min:
                text_color=cfg.c_text_warn_color
            else:
                text_color=cfg.c_text_info_color
            self.cw.set_info_line_2(cfg.info_line.format('Backup System', self.obs2.obs_status, self.obs2.disk_space/1024 ), text_color) 

        if self.usb_drive != '':
            usb_free_disk = disk_usage('{}:\\'.format(self.usb_drive)).free / 1024 / 1024 / 1024
            text_color=cfg.c_text_info_color
            self.cw.set_info_line_3(cfg.info_line.format('USB Drive', 'available', usb_free_disk), text_color)

        self.wm.after(cfg.fd_delay, self.update_sys_lines) 

    def get_drives(self): # return a list of current drives
        drive_list = []
        disk_info = disk_partitions()
        for drive in disk_info:
            if 'removable' in drive.opts.lower():
                drive_list.append(drive.mountpoint[0])
        if self._debug: print(f'>>> disk_info: {disk_info}\n>>> drive_list: {drive_list}')
        return drive_list

    def debug_exit(self, e):
        self.cw.withdraw()     
        self.wm.after_cancel(self.update_state)     
        self.cw.set_state_line(f'\n>>> debug_exit: initiated with {e}', cfg.state_font_color)
        print(f'\n>>> debug_exit: initiated with {e}')
        self.wm.after_cancel(self.update_sys_lines) 
        self.tw.destroy()   
        self.kb.destroy()    
        if self.state == Recording_State.RECORDING:
            self.obs1.stop_recording()
        self.obs1.__del__()
        if cfg.obs2_host != '':
            self.obs2.__del__()  
        self.cw.destroy()
        self.wm.destroy()
        exit(17)

if __name__ == '__main__':
    st = Story_Room()
    st.wait_for_drive() # drive insertion starts a recording session
