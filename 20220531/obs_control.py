"""
    simpler interface to websockets using simpleobsws
"""
import asyncio
import simpleobsws

class Obs_Control( ):
    
    pswd = 'family'

    free_disk = 0
    obs_status = ''
    obs_version_text = ''
    ws_version = ''


    def __init__( self ):
        self.loop = asyncio.get_event_loop()
        self.ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password=self.pswd, loop=self.loop)

    # get OBS status
    async def __obs_version( self ):
        # global obs_version, ws_version
        await self.ws.connect()
        info = await self.ws.call( 'GetVersion' )
        self.obs_version_text = info[ 'obs-studio-version' ]
        self.ws_version = info[ 'obs-websocket-version' ]
        await asyncio.sleep( 1 )
        await self.ws.disconnect()
        # TODO: set in caller: var.set( f'obs {rc["obs-studio-version"]}, ws {rc["obs-websocket-version"]}, status {rc["status"]}' ) 

    async def obs_version( self ):
        self.loop.run_until_complete( self.__obs_version( ) )

    # get environmental info from OBS
    async def __get_stats( self ):
        global free_disk, obsstatus
        await self.ws.connect()
        rc = await self.ws.call( 'GetStats' )
        print( f'GetStats: {rc}' )
        await asyncio.sleep( 1 )
        await self.ws.disconnect()
        free_disk = str( int( float( rc[ 'stats' ][ 'free-disk-space'] ) ) )
        obsstatus = rc[ 'status' ]
        #TODO: figure out what and how to return

    def get_stats( self ):
        self.loop.run_until_complete( self.__get_stats( ) )

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


    async def test_request( self ):
        await self.ws.connect() # Make the connection to OBS-Websocket
        result = await self.ws.call('GetVersion') # We get the current OBS version. More request data is not required
        print( f'OBS version: {result[ "obs-studio-version" ]}, websocket version: { result[ "obs-websocket-version" ] } ') # Print the raw json output of the GetVersion request
        await asyncio.sleep(1)
        data = {'source':'Video Capture Device', 'volume':0.5}
        result = await self.ws.call('SetVolume', data) # Make a request with the given data
        print( f'Status of VidCap device: {result[ "status" ] } ' )
        await self.ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.
        return f'{result[ "status" ] }'

# === end of class Obs_Control ===


# test code here
#async def testit( obs ):
#    await obs.obs_version()
#    print( f'OBS version: {obs.obs_version}, websocket version: { obs.ws_version } ')
#    bar = await obs.test_request( )
#    print( f'bar be {bar}' )
#
#def main( ):
#    obs = Obs_Control( )
#    obs.loop. ( testit( obs ))
#
#if __name__ == '__main__':
#    main()
#
