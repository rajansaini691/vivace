import threading
import time
import asyncio
import websockets
"""
The main server writing the RGB array to a websocket. A client can then render
a simulated version of the LED strip in the browser over a LAN.
"""


# TODO Delete when done
def vivace_test_main(cv, pixel_map):
    """
    Simulates generation of the pixel map
    """
    while(True):
        with cv:
            for i in range(len(pixel_map)):
                pixel_map[i] += 1
                pixel_map[i] %= 255
            cv.notifyAll()
        time.sleep(0.05)


async def write_socket(websocket, path, cv, arr):
    """
    Feeds the given array to the websocket as the array gets updated
    """
    while True:
        with cv:
            cv.wait()
            byte_array = bytes(arr)
        await websocket.send(byte_array)


def vivace_server_thd(cv, pixel_map):
    """
    Main thread that feeds the pixel map to a web socket
    """
    # Start asynchronous event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        websockets.serve(lambda websocket, path, arg=(cv, pixel_map):
                         write_socket(websocket, path, cv, pixel_map),
                         'localhost', 4444))
    loop.run_forever()


# TODO Delete when done testing
if __name__ == '__main__':
    # Stores when the rgb array is ready for consumption
    array_ready = threading.Condition()
    test_pixel_map = [500, 501, 502]
    test_main_thd = threading.Thread(name='test_main', target=vivace_test_main,
                                     args=(array_ready, test_pixel_map))
    server_thd = threading.Thread(name='server_thd', target=vivace_server_thd,
                                  args=(array_ready, test_pixel_map))

    test_main_thd.start()
    server_thd.start()
