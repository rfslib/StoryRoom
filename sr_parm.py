"""
    file: sr_parm.py
    Author: rfslib
    
    purpose: configuration parameters for story_room.pyw
"""

class SR_Parm():

    # strings
    timer_waiting_message = 'Riverton Story Room'
    start_btn_txt = 'Start\nSession'
    stop_btn_txt = 'End\nSession'
    ttl = 'Story Room'       # control window title

    # configuration stuff
    countdown_to_start = 20 # 20 seconds
    recording_length = 3600 # one hour of recording = 3600 seconds
    recording_warn_at = 120 # seconds before end of recording to start warning message

    # control_window
    bg_color = 'LightGreen' # 'SystemButtonFace'
    bg_alpha = 0.95,
    text_info_color = 'Black'
    text_warn_color = 'Red'
    text_done_color = 'DarkGreen'
    text_soft_color = 'Grey'
    font_family = 'Consolas'
    font_bold = 'Consolas Bold'
    font_italic = 'Consolas Italic'
    btn_height = 4
    btn_fontsize = 24
    btn_idle_color = 'Grey'
    btn_active_color = 'Red'
    btn_bg_color = 'SystemButtonFace'

    font = 'Lucida Console'    # primary font for text
    fontsize = 48              # font size
    fontcolor = '#100010'
    ##bgcolor = '#efffef'             # background color
    padxy = 4                   # padding inside of frames
    info_fontsize = 10
    info_fontcolor = 'grey'

    free_disk_min = 5000.0 # minimum available space on disk before displaying warning
    fd_delay = 20000  # 60000 to update available disk space once a minute

    # OBS
    obs_processname = 'obs64.exe'
    obs_start_wait_tries = 8 # The first time after a reboot may take a while
    obs_start_wait_delay = 2
    obs_command = r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'
    obs_directory = r'C:\Program Files\obs-studio\bin\64bit'
    obs_startup_parms = '--disable-updater'
    obs_output_destination = r'C:\Users'

    # OBS interface
    obs_pswd = 'family'
    obs_host = '127.0.0.1'
    obs_port = 4444

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
    tw_warnbg = 'DarkRed'
    tw_normalpha = 0.5
    tw_warnalpha = 0.9
    tw_padxy = 4                   # padding inside of frames
    tw_btn_fontsize = 12

    # expected (tested) versions
    expected_obs_version = '27.2.4'
    expected_ws_version = '4.9.1'
    expected_simpleobsws_version = '1.1'