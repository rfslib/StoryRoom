"""
    file: sr_parm.py
    Author: rfslib
    
    purpose: configuration parameters for story_room.pyw
"""

class SR_Parm():

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
    fd_delay = 5000  # 60000 to update available disk space once a minute

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

    # expected (tested) versions
    expected_obs_version = '27.2.4'
    expected_ws_version = '4.9.1'
    expected_simpleobsws_version = '1.1'