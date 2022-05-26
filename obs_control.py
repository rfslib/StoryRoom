"""
    simpler interface to websockets using simpleobsws
"""
import asyncio
import simpleobsws

class Obs_Control( ):
    
    pswd = 'family'

    def __init__( self ):
        self.loop = asyncio.get_event_loop()
        self.ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='family', loop=self.loop)

    # get OBS status
    async def obs_status( self, var ):
        global info_line
        await self.ws.connect()
        rc = await self.ws.call( 'GetVersion' )
        await asyncio.sleep( 1 )
        await self.ws.disconnect()
        var.set( f'obs {rc["obs-studio-version"]}, ws {rc["obs-websocket-version"]}, status {rc["status"]}' ) 

    # get environmental info from OBS
    async def get_stats( self ):
        global free_disk, obsstatus
        await self.ws.connect()
        rc = await self.ws.call( 'GetStats' )
        print( f'GetStats: {rc}' )
        await asyncio.sleep( 1 )
        await self.ws.disconnect()
        free_disk = str( int( float( rc[ 'stats' ][ 'free-disk-space'] ) ) )
        obsstatus = rc[ 'status' ]
        #TODO: figure out what and how to return

    async def start_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StartRecording' )
        print( f'start_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )

    async def stop_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StopRecording' )
        print( f'stop_recording rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )

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
async def testit():
    foo = Obs_Control()
    bar = await foo.test_request( )
    print( f'bar be {bar}' )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete( testit() )
