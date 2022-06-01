"""
    file: control_window.py
    author: ed c
"""
import asyncio
import simpleobsws
from tkinter import *

import time

import timer_window

class Control_Window( Toplevel ):

    debug = 1

    # configuration stuff
    timer_waiting_message = 'Riverton Story Room'
    countdown_to_start = 20 # 20 seconds
    recording_length = 3600 # one hour of recording = 3600 seconds
    recording_warn_at = 120 # seconds before end of recording to start warning message

    # visuals
    start_btn_txt = 'Start Session'
    start_btn_height = 4
    start_btn_fontsize = 12

    ## attributes of the control window
    moffsetx = 0
    moffsety = 0
    ttl = 'Story Room'       # title
    font = 'Lucida Console'    # primary font for text
    fontsize = 48              # font size
    fontcolor = '#100010'
    bgcolor = '#efffef'             # background color
    padxy = 4                   # padding inside of frames
    info_fontsize = 10
    info_fontcolor = 'grey'
    #infoline = '' # StringVar, created in __init__, see getter and setter
    
    # OBS info
    pswd = 'family'
    obs_version = ''
    ws_version = ''
    obs_status = ''

    # environment info
    free_disk = 0.0

    def __init__( self, master ):
        Toplevel.__init__(self,master)

        # set our look
        self.config( bg=self.bgcolor)
        self.overrideredirect( True )
    
        # get our size and location
        self.mwidth = self.winfo_screenwidth( )
        self.mheight = self.winfo_screenheight( )
        if self.debug:
            self.mwidth = int( self.mwidth / 2 ) 
            self.mheight = int( self.mheight / 2 ) 
            self.moffsetx = 48
            self.moffsety = 48
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')
        if self.debug: print( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )

        # set up the window's "title" frame
        self.ttlframe = Frame( master=self,
            relief = RIDGE, borderwidth = 5, bg=self.bgcolor,
            padx = self.padxy, pady = self.padxy )
        self.ttlframe.grid( row=0, column=0, padx = self.padxy, pady = self.padxy, sticky='ew' )
        self.grid_columnconfigure( 0, weight=1 )
        Label( master=self.ttlframe, # width=30,
            text=self.ttl, font=('Lucida Console', self.fontsize), bg=self.bgcolor, fg=self.fontcolor,
            ).pack( padx = self.padxy, pady = self.padxy)

        # set up an interface to OBS Studio
        self.loop = asyncio.get_event_loop()
        self.ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password=self.pswd, loop=self.loop)

        # get some info from OBS
        self.loop.run_until_complete( self.get_obs_info( ) )

        # "info" frame
        self._infoline=StringVar()
        self._diskline=StringVar()
        self.set_infoline( f'OBS Studio version: {self.obs_version}, Websockets version: {self.ws_version}' )
        self.set_diskline( f'Free Disk Space: {self.free_disk / 1024:.1f}G')
        self.infframe = Frame( master=self,
            bg=self.bgcolor, padx=self.padxy, pady=self.padxy )
        self.infframe.grid( row=6, column=0, padx=self.padxy, pady=self.padxy, sticky = 'es' )
        inflabel = Label( master=self.infframe, text=self._infoline.get(), fg=self.info_fontcolor,
            font=( 'Lucida Console', self.info_fontsize ) ).pack( padx=self.padxy, pady=self.padxy )
        dsklabel = Label( master=self.infframe, text=self._diskline.get(), fg=self.info_fontcolor,
            font=( 'Lucida Console', self.info_fontsize ) ).pack( padx=self.padxy, pady=self.padxy )

        # create a frame for interactions (buttons, text entry, etc.)
        self.btnframe = Frame( master=self, 
            padx = self.padxy, pady = self.padxy )
        self.btnframe.grid( row=2, column=0, padx = self.padxy, pady = self.padxy, sticky='ewn' )
        #Label( master=self.btnframe, text='' ).pack( padx = self.padxy, pady = self.padxy )
              
        self.ctrl_strt= Button( self.btnframe, text = self.start_btn_txt,
            height=self.start_btn_height,
            command = self.schedule_recording,
            font = ( self.font, self.start_btn_fontsize ) ).pack()

        if self.debug: print( 'control window ready' )

        # set up the timer window
        self.tw = timer_window.Timer_Window( master )
        self.tw.set_txt( self.timer_waiting_message )
        if self.debug: print( 'timer window ready' )

        if self.debug: print( 'system ready' )


# ----

    async def get_obs_info( self ):
        await self.ws.connect()
        info = await self.ws.call( 'GetVersion' )
        if self.debug: print( f'GetVersion: {info}')
        self.obs_version = info[ 'obs-studio-version' ]
        self.ws_version = info[ 'obs-websocket-version' ]
        stats = await self.ws.call( 'GetStats' )
        if self.debug: print( f'GetStats: {stats}')
        self.free_disk = float( stats[ 'stats' ][ 'free-disk-space' ] )
        await asyncio.sleep( 1 )
        await self.ws.disconnect()

    async def __start_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StartRecording' )
        print( f'start_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )

    def start_recording( self ):
        self.loop.run_until_complete( self.__start_recording( ) )

    async def __stop_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StopRecording' )
        print( f'stop_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )

    def stop_recording( self ):
        self.loop.run_until_complete( self.__stop_recording( ) )

    def test_callback( self ):
        print( 'test_callback called' )

    def schedule_recording( self ):
        self.tw.start_countdown( 'starting in {} seconds', 20, 1, 10, self.test_callback )

    def start_session():
        pass

    def get_infoline( self ):
        return self._infoline.get()

    def set_infoline( self, textin ):
        self._infoline.set( str( textin ) )
        #TODO: isn't this supposed to be automagic? self.infframe.update()
    
    def get_diskline( self ):
        return self._diskline.get()

    def set_diskline( self, textin ):
        self._diskline.set( str( textin ) )
    

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+48' )
    root.title( 'close me to exit test' )
    tst = Control_Window( root )
    #tst.start_recording( )
    #time.sleep( 3 )
    #tst.stop_recording( )
    root.mainloop()
