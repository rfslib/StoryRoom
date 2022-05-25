import logging
logging.basicConfig(filename='debuglog.log', level=logging.DEBUG)
import asyncio
import simpleobsws

parameters = simpleobsws.IdentificationParameters() # Create an IdentificationParameters object
parameters.eventSubscriptions = (1 << 0) | (1 << 2) # Subscribe to the General and Scenes categories


ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4444', password = 'family', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.
print( f'ws: {ws}' )

async def on_event(eventType, eventData):
    print('New event thingie! Type: {} | Raw Data: {}'.format(eventType, eventData)) # Print the event data. Note that `update-type` is also provided in the data
    logging.debug('New event thingie! Type: {} | Raw Data: {}'.format(eventType, eventData)) # Print the event data. Note that `update-type` is also provided in the data

async def on_switchscenes(eventData):
    print('Scene switched to "{}".'.format(eventData['sceneName']))
    logging.debug('Scene switched to "{}".'.format(eventData['sceneName']))

async def init():
    await ws.connect()
    await ws.wait_until_identified()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
ws.register_event_callback(on_event) # By not specifying an event to listen to, all events are sent to this callback.
ws.register_event_callback(on_switchscenes, 'SwitchScenes')
loop.run_forever()