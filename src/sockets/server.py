import threading
import time
import asyncio
import websockets
import http.server
import socketserver
from server_conf import SocketConf
"""
Simulates the LED strip using an HTTP server with websockets. Used for
development and offsite testing.
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
        await asyncio.sleep(0.01)


def vivace_socket_thd(cv, pixel_map):
    """
    Feeds the pixel map to a web socket
    """
    # Start asynchronous event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(lambda websocket, path, arg=(cv,
                              pixel_map): write_socket(websocket, path,
                              cv, pixel_map), '0.0.0.0', 4444)

    loop.run_until_complete(server)
    loop.run_forever()


def vivace_server_thd():
    """
    Starts and runs the HTTP server
    """
    # Start HTTP Server
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", SocketConf.PORT), Handler) as httpd:
        print("serving at port", SocketConf.PORT)
        httpd.serve_forever()


# TODO Delete when done testing
if __name__ == '__main__':
    # Stores when the rgb array is ready for consumption
    array_ready = threading.Condition()
    test_pixel_map = [500, 501, 502]
    test_main_thd = threading.Thread(name='test_main', target=vivace_test_main,
                                     args=(array_ready, test_pixel_map))
    socket_thd = threading.Thread(name='socket_thd', target=vivace_socket_thd,
                                  args=(array_ready, test_pixel_map))
    server_thd = threading.Thread(name='server_thd', target=vivace_server_thd)

    test_main_thd.start()
    socket_thd.start()
    server_thd.start()
