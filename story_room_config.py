"""
    file: sr_parm.py
    Author: rfslib
    
    purpose: configuration parameters for story_room.pyw
"""
'''
A class for the current program state
'''
from enum import Enum # , auto

class RecordingState(Enum):
    INIT = 'Initializing the system'           # program initialization
    DRIVE_ALREADY = 'There\'s a USB drive mounted. Please remove it to proceed...'
    WAIT_FOR_DRIVE = 'System Ready. Insert a new USB drive to begin...' # ready to record
    DRIVE_INSERTED = 'Drive attached.' # a removable drive has been connected
    GET_FILENAME = 'Enter a name for the video file...'   # get the final filename
    WAIT_FOR_START = 'Everything is ready. Tap the "Start Recording" button to begin...' # ready to record, waiting for go to start countdown
    COUNTDOWN = 'Counting down to start of recording. You can leave the room now :)'      # countdown to start of recording is in progress
    RECORDING = 'Recording. Please wait (or press the stop button to end it early).'      # recording is in progress
    ABORTING = 'Early stop of the recording requested.'       # early stop of recording was requested
    FINISHING = 'Stopping the Recording.'     # recording stop has been requested
    FINISHED = 'Recording has stopped. Re-muxing the file and preparing to copy to the USB drive.'       # recording has stopped (reMUX in progress)
    COPYING = 'Copying the video file to the USB drive. Please wait...'        # video file is being copied to removable drive
    COPY_FAILED = 'Copy to USB drive failed. See the recovery procedure in the usage guide.'
    DRIVE_READY = 'Copy to the USB drive is complete. Please remove the drive now...'    # copy is complete, waiting for drive to be removed
    DRIVE_REMOVED = 'USB Drive removed. Bringing out the janitorial supplies.'  # drive removed
    CLEANUP = 'Recording session is over. Preparing the system for the next session.'        # cleanup in progress: extra files being removed, session being reset


class StoryRoomConfiguration():

    # strings
    c_title_text = 'Riverton FamilySearch Story Room'
    timer_waiting_message = 'Riverton Story Room'
    start_btn_txt = 'Start\nRecording'
    stop_btn_txt = 'Stop\nRecording'
    ttl = 'Story Room'       # control window title
    info_line = '{} Status: {}, Available disk space: {:.1f}G'
    t_leadin_msg = 'Start recording in {} seconds' # what displays on the monitor (projector) screen
    t_wait_for_start_msg = 'Starting...please wait'
    t_record_msg = 'Recording time remaining: {} minutes'
    t_end_msg = 'Recording time remaining: {} seconds'
    c_time_left_msg = '{} minutes left'
    c_main_system_name = 'Main System'
    c_backup_system_name = 'Backup System'
    c_backup_unavailable_msg = 'Backup system is not available'
    c_usb_remove_msg = 'Please remove the USB drive'
    c_usb_status_hdr = 'USB Drive'
    c_usb_info_line = '{}, Available disk space: {:.1f}G'

    # timer usage stuff
    t_drift = 1 # for test computer: 1-(100/3600) # allow time for processing between .after calls; varies per machine
    t_leadin_to_start = 20 # 20                         # length of the countdown (in seconds)
    t_leadin_warn_at = 20                          # when to set to warning color (in seconds)
    t_leadin_return_at = 1                         # when to call the callback
    t_record_interval = 60                         # how often to update the display (in seconds)
    t_record_length = 3600 # 3600                         # one hour of recording = 3600 seconds
    t_record_warn_at = 120 # 120                         # seconds before end of recording to start warning color change
    t_record_return_at = 60                        # seconds before record_length to call the callback
    #tw_end_length = recording_return_at
    t_end_interval = 1
    #tw_end_warn_at = recording_return_at

    # control_window
    c_title_fontsize = 36
    c_bg_color = 'antique white' #'LightGreen' # 'SystemButtonFace'
    c_bg_alpha = 0.95
    c_text_info_color = 'Black'
    c_text_warn_color = 'Red'
    c_text_done_color = 'DarkGreen'
    c_text_soft_color = 'Grey'
    c_text_font = 'Consolas'
    c_bold_font = 'Consolas Bold'
    c_italic_font = 'Consolas Italic'
    c_btn_height = 4
    c_btn_fontsize = 24
    c_btn_idle_color = 'linen' # 'LightGrey'
    c_btn_active_color = 'Red'
    c_btn_bg_color = 'misty rose' #'SystemButtonFace'
    c_time_left_fontsize = 84

    #font = 'Lucida Console'    # primary font for text
                  # font size
    fontcolor = '#100010'
    padxy = 2                   # padding inside of frames
    c_info_fontsize = 16
    info_fontcolor = 'grey'
    c_state_fontsize = 16
    c_state_font_color = 'Navy' # 'DarkBlue'

    free_disk_min = 3000.0 # minimum available space on disk before displaying warning
    update_obs_status_delay = 5000
    update_usb_status_delay = 1000
    ##fd_delay = 2500 # time between updates to OBS and USB status lines

    # OBS
    obs_processname = 'obs64.exe'
    obs_start_wait_tries = 8 # The first time after a reboot may take a while
    obs_start_wait_delay = 2
    obs_command = r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'
    obs_directory = r'C:\Program Files\obs-studio\bin\64bit'
    obs_startup_parms = '--disable-updater'
    obs_output_destination = r'C:\Users'

    # OBS interface
    obs1_host = '127.0.0.1'
    obs1_port = 4444
    obs1_pswd = 'family'
    obs2_host = '192.168.74.74' #give a host name/ip address to activate second system
    obs2_port = 4444
    obs2_pswd = 'family'

    # timer_window

    ## attributes of the timer window
    tw_mwidth = 1920
    tw_yoffset = 0
    tw_xoffset = 0
    tw_mheight = 100
    tw_font = 'Lucida Console'    # primary font for text
    tw_fontsize = 64              # font size
    tw_fontcolor = 'DarkGrey'
    tw_fontwarn = 'Black' # 'DarkRed'
    tw_normbg = 'Grey' # 'Grey'
    tw_warnbg = 'tomato'
    tw_normalpha = 0.5
    tw_warnalpha = 0.9
    tw_padxy = 4                   # padding inside of frames
    tw_btn_fontsize = 12

    # oops window
    o_bg_color = 'SkyBlue1'
    o_fg_color = 'Black'
    o_text_font = 'Lucida Console Bold'
    o_text_fontsize = 13
    o_btn_font = 'Lucida Console'
    o_btn_fontsize = 24
    o_btn_height = 2

    # expected (tested) versions
    expected_obs_version = '27.2.4'
    expected_ws_version = '4.9.1'
    expected_simpleobsws_version = '1.1'