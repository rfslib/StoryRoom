import asyncio
import simpleobsws
import time

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='family', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to OBS-Websocket
    result = await ws.call('GetVersion') # We get the current OBS version. More request data is not required
    print( f'OBS version: {result[ "obs-studio-version" ]}, websocket version: { result[ "obs-websocket-version" ] } ') # Print the raw json output of the GetVersion request
    await asyncio.sleep(1)
    data = {'source':'Video Capture Device', 'volume':0.5}
    result = await ws.call('SetVolume', data) # Make a request with the given data
    print( f'Status of VidCap device: {result[ "status" ] } ' )
    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

async def get_stats():
    await ws.connect()
    rc = await ws.call( 'GetStats' )
    print( f'GetStats: {rc}' )
    await asyncio.sleep( 1 )
    await ws.disconnect()

async def start_recording():
    await ws.connect()
    rc = await ws.call( 'StartRecording' )
    print( f'rc: {rc}')
    await asyncio.sleep( 1 )
    await ws.disconnect( )

async def stop_recording():
    await ws.connect()
    rc = await ws.call( 'StartStopRecording' )
    print( f'rc: {rc}')
    await asyncio.sleep( 1 )
    await ws.disconnect( )

loop.run_until_complete(make_request() )
#loop.run_until_complete( get_stats() )
loop.run_until_complete(start_recording() )
time.sleep( 3 )
#loop.run_until_complete( get_stats() )
loop.run_until_complete( stop_recording() )
#loop.run_until_complete( get_stats() )
