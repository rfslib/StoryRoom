"""
    file: obs_xface.py
    author: rfslib
    
    purpose: a simplified interface to manage obs startup and status for story_room
"""

#from signal import raise_signal
from sr_parm import SR_Parm as parms

import asyncio
from simpleobsws import obsws
import psutil
import subprocess
from time import sleep

debug = True

class OBS_Error(Exception):
    pass

class OBS_Xface(obsws):

    def __init__(self, host='localhost', port=4444, password=None, call_poll_delay=100, loop: asyncio.BaseEventLoop=None, callback=None, local=True):
        super().__init__(host, port, password)
        self.debug = True
        # Set up our local variables
        self.host = host
        self.port = port
        self.password = password
        self.call_poll_delay = call_poll_delay
        self.obs_version = ''
        self.ws_version = ''
        self.obs_status = ''

        # gonna need an asyncio event loop
        self.loop = loop
        if self.loop == None:
            self.loop = asyncio.get_event_loop()
        self.callback = callback # callback to handle websocket events

        # start OBS if it isn't already running
        print('OBS_Xface checking if obs is running')
        if self.obs_is_running():
            print('we think OBS is running; going to register on_obs_event')
            self.loop.run_until_complete(self.connect())
            self.register(self.on_obs_event) # handle events
            self.loop.run_until_complete(self.get_obs_info()) # get the basic info (version, status, etc.)
        else:
            print('we didn\'t get OBS to run; returning None')
            raise OBS_Error("could not start OBS")

        #self.loop.run_until_complete(self.connect())

    #def __del__(self):
    #    self.loop.run_until_complete(self.disconnect())
    #    self.loop.close()

    async def get_obs_info(self):
        #await self.connect()
        info = await self.call( 'GetVersion' )
        if self.debug: print( f'GetVersion: {info}')
        self.obs_version = info['obs-studio-version']
        self.ws_version = info['obs-websocket-version']
        self.obs_status = info['status']
        await asyncio.sleep( 1 )
        stats = await self.call( 'GetStats' )
        if self.debug: print( f'GetStats: {stats}')
        await asyncio.sleep( 1 )
        #await self.disconnect()

    def is_process_running(self, processName):
        # scan all the running processes for processName
        if debug: print(f'checking if {processName} is running')
        for proc in psutil.process_iter():
            if processName.lower() in proc.name().lower():
                if debug: print('OBS runneth')
                return True
        if debug: print('OBS doth NOT run')
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
                if debug: print('OK, let\'s get OBS running...')
                foo = subprocess.Popen(parms.obs_command, cwd=parms.obs_directory)
                if debug: print(f'foo: {foo}')
            except:
                return False
            # wait for OBS to start (TODO: there's probably a better way to do this...)
            obs_ready = False
            wait_attempts = 0
            while wait_attempts < parms.obs_start_wait_tries and obs_ready == False:
                sleep(parms.obs_start_wait_delay)
                print(f'running: {self.is_process_running(parms.obs_processname)}')
                if self.is_process_running(parms.obs_processname):
                    obs_ready = True
            sleep(2) # let OBS settle before hammering it with requests
            return obs_ready

    async def on_obs_event(self, data):
        print( f'OBS Event: \'{data["update-type"]}\', Raw data: {data}')
        if self.callback != None:
            await self.callback(data)
        
    async def __start_recording( self ):
        #await self.connect()
        rc = await self.call( 'StartRecording' )
        print( f'start_recording rc: {rc}')
        await asyncio.sleep( 1 )
        #await self.disconnect( )

    def start_recording( self ):
        self.loop.run_until_complete( self.__start_recording( ) )

    async def __stop_recording( self ):
        #await self.connect()
        rc = await self.call( 'StopRecording' )
        print( f'stop_recording rc: {rc}')
        await asyncio.sleep( 1 )
        #await self.disconnect( )

    def stop_recording( self ):
        self.loop.run_until_complete( self.__stop_recording( ) )
