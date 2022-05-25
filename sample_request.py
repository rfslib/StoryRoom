import logging
logging.basicConfig(filename='sample_request.log', level=logging.DEBUG)
import asyncio
import simpleobsws

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4444', password = 'family', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    print('connection request made')
    await ws.wait_until_identified() # Wait for the identification handshake to complete
    print('connection request acknowledged')

    request = simpleobsws.Request('GetVersion') # Build a Request object
    print( f'request built: {request}')

    """
    ret = await ws.call(request) # Perform the request
    print('call returned')
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
    else:
        print('request not ok: {}'.format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly
    print('disconnected')
    """

loop = asyncio.get_event_loop()
print('ok, here we go...')
loop.run_until_complete(make_request())