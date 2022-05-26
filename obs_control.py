"""
    simpler interface to websockets using simpleobsws
"""
import asyncio
import simpleobsws

class Obs_Control( ):
    
    pswd = 'family'

    def __init__( self ):
        loop = asyncio.get_event_loop()
        ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='family', loop=loop)

    async def make_request( self ):
        await self.ws.connect() # Make the connection to OBS-Websocket
        result = await self.ws.call('GetVersion') # We get the current OBS version. More request data is not required
        print( f'OBS version: {result[ "obs-studio-version" ]}, websocket version: { result[ "obs-websocket-version" ] } ') # Print the raw json output of the GetVersion request
        await asyncio.sleep(1)
        data = {'source':'Video Capture Device', 'volume':0.5}
        result = await self.ws.call('SetVolume', data) # Make a request with the given data
        print( f'Status of VidCap device: {result[ "status" ] } ' )
        await self.ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

    async def start_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StartRecording' )
        print( f'rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )

    async def stop_recording( self ):
        await self.ws.connect()
        rc = await self.ws.call( 'StopRecording' )
        print( f'rc: {rc}')
        await asyncio.sleep( 1 )
        await self.ws.disconnect( )


# test code here
async def testit():
    foo = Obs_Control()
    await foo.make_request( )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete( testit() )
