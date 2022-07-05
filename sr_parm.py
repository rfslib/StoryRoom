"""
    file: sr_parm.py
    Author: rfslib
    
    purpose: configuration parameters for story_room.pyw
"""

class SR_Parm():

    # control_windows
    bg_color = 'SystemButtonFace'
    bg_alpha = 0.95,
    text_info_color = 'Black'
    text_warn_color = 'Red'
    text_done_color = 'DarkGreen'
    text_soft_color = 'Grey'
    font_family = 'Consolas'
    font_bold = 'Consolas Bold'
    font_italic = 'Consolas Italic'

    free_disk_min = 5000.0 # minimum available space on disk before displaying warning
    fd_delay = 20000  # 60000 to update available disk space once a minute

    # OBS
    obs_processname = 'obs64.exe'
    obs_command = r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'
    obs_directory = r'C:\Program Files\obs-studio\bin\64bit'
    obs_startup_parms = '--disable-updater'
    obs_output_destination = r'C:\Users'

    # OBS interface
    obs_pswd = 'family'
    obs_host = '127.0.0.1'
    obs_port = 4444

    # timer_window
    ## countdown stuff
    tw_countdown_seconds = 10
    tw_countdown_active = False
    tw_countdown_complete = False
    tw_countdown_interval = 1
    tw_countdown_warn = 5
    tw_countdown_string = '{} seconds remaining'

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