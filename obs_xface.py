"""
    file: obs_xface.py
    author: rfslib
    
    purpose: a simplified interface to manage obs startup and status for story_room
"""

from signal import raise_signal
from sr_parm import SR_Parm as parms

import asyncio
from simpleobsws import obsws
import psutil
from time import sleep

class OBS_Xface(obsws):

    def __init__(self, host='localhost', port=4444, password=None, call_poll_delay=100, loop: asyncio.BaseEventLoop=None, callback=None):
        super().__init__(host, port, password)
        self.debug = True

        self.host = host
        self.port = port
        self.password = password
        self.call_poll_delay = call_poll_delay
        self.loop = loop
        if self.loop == None:
            self.loop = asyncio.get_event_loop()
        self.callback = callback
        self.obs_version = ''
        self.ws_version = ''
        self.obs_status = ''
        if self.obs_is_running():
            self.register(self.on_obs_event)
            self.loop.run_until_complete(self.get_obs_info())

        else:
            return None

    async def get_obs_info(self):
        await self.connect()
        info = await self.call( 'GetVersion' )
        #if self.debug: print( f'GetVersion: {info}')
        self.obs_version = info['obs-studio-version']
        self.ws_version = info['obs-websocket-version']
        self.obs_status = info['status']
        await asyncio.sleep( 1 )
        stats = await self.call( 'GetStats' )
        #if self.debug: print( f'GetStats: {stats}')
        await asyncio.sleep( 1 )
        await self.disconnect()

    def is_process_running(self, processName): # https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
        '''
        Check if there is any running process that contains the given name processName.
        '''
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except: # (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return False

    def obs_is_running(self):
        '''
        returns: 
            True if OBS is running
            False if failure to start
        '''
        # be sure OBS is running
        if self.is_process_running(parms.obs_processname):
            return True
        else:
            try:
                asyncio.subprocess.Popen(parms.obs_command, cwd=parms.obs_directory)
                sleep(5)
                return self.is_process_running(parms.obs_processname)
            except:
                return False

    async def on_obs_event(self, data):
        print( f'OBS Event: \'{data["update-type"]}\', Raw data: {data}')
        await self.callback(data)
        #self.loop.run_until_complete(self.callback(data))
        
    async def __start_recording( self ):
        await self.connect()
        rc = await self.call( 'StartRecording' )
        print( f'start_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.disconnect( )

    def start_recording( self ):
        self.loop.run_until_complete( self.__start_recording( ) )

    async def __stop_recording( self ):
        await self.connect()
        rc = await self.call( 'StopRecording' )
        print( f'stop_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.disconnect( )

    def stop_recording( self ):
        self.loop.run_until_complete( self.__stop_recording( ) )
