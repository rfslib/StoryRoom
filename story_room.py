"""
    file: story_room.py
    author: Ed C

    references:
        https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python

    purpose: start Tk and set up windows for control of the Story Room recording system
            meant to run continuously
"""

from shutil import disk_usage
from time import time
from tkinter import *

# our classes for the two windows
from control_window import Control_Window
from timer_window import Timer_Window

# for websocket interface to OBS Studio
import asyncio
import simpleobsws

debug = 1
info_line = ''
free_disk = 0 # in megabytes
obsstatus = ''

# for websockets interface to OBS Studio
loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='family', loop=loop)

# get OBS status
async def obs_status():
    global info_line
    await ws.connect()
    rc = await ws.call( 'GetVersion' )
    await asyncio.sleep( 1 )
    await ws.disconnect()
    info_line = f'obs {rc["obs-studio-version"]}, ws {rc["obs-websocket-version"]}, status {rc["status"]}'

# get environmental info from OBS
async def get_stats():
    global free_disk, obsstatus
    await ws.connect()
    rc = await ws.call( 'GetStats' )
    print( f'GetStats: {rc}' )
    await asyncio.sleep( 1 )
    await ws.disconnect()
    free_disk = str( int( float( rc[ 'stats' ][ 'free-disk-space'] ) ) )
    obsstatus = rc[ 'status' ]

# tell OBS to start recording
async def start_recording():
    await ws.connect()
    rc = await ws.call( 'StartRecording' )
    print( f'rc: {rc}')
    await asyncio.sleep( 1 )
    await ws.disconnect( )

# tell OBS to stop recording
async def stop_recording():
    await ws.connect()
    rc = await ws.call( 'StopRecording' )
    print( f'rc: {rc}')
    await asyncio.sleep( 1 )
    await ws.disconnect( )

def session():
    # get OBS status
    loop.run_until_complete(get_stats())

    # get file name
    # start countdown to go live (on monitor)
    # start recording
    # start countdown to end of recording (on monitor)
    # loop to show stats (on control)
    # check if recording stopped early
    # stop recording
    # display status message ("copying") (on monitor and control)
    # copy to usb drive
    # display "done" (on monitor and control)
    # reset everything
    # clear displays, return to control

# Tk event callback
def callback_test( ):
    print( 'callback called :)')
    timer_win.set_txt( 'YAY!')
    timer_win.start_countdown( 'remaining minutes: {}', 120, 60, 60, callback_test )


#set up window manager
wm = Tk()

if debug: # show the root window so it can be closed to exit the test
    wm.geometry( '400x100+0+0' )
    wm.title( 'Close me to shut down the test' )
else: # but normally hide the root window
    wm.withdraw()

loop.run_until_complete(obs_status())
loop.run_until_complete(get_stats())
control_win = Control_Window( wm)
control_win.set_infoline( info_line )
control_win.set_diskline( disk_usage)
timer_win = Timer_Window( wm )

if debug: timer_win.start_countdown( 'starting in {} seconds', 5, 1, 3, callback_test )

wm.mainloop() # make Tk work
print( '=== after mainloop ===')

