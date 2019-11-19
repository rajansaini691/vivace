import threading
import time
"""
The main server writing the RGB array to a websocket. A client can then render
a simulated version of the LED strip in the browser over a LAN.
"""


# TODO Delete when done
def vivace_test_main(cv, test_rgb_array):
    i = 0
    while(True):
        with cv:
            test_rgb_array.append(i)
            cv.notifyAll()
        time.sleep(0.5)


def vivace_server_thd(cv, test_rgb_array):
    while(True):
        with cv:
            cv.wait()
            # TODO Log to file
            print(test_rgb_array)
        time.sleep(1)


# TODO Delete when done
if __name__ == '__main__':
    # Stores when the rgb array is ready for consumption
    array_ready = threading.Condition()
    test_rgb_array = [1, 2, 3]
    test_main_thd = threading.Thread(name='test_main', target=vivace_test_main,
                                     args=(array_ready, test_rgb_array))
    server_thd = threading.Thread(name='server_thd', target=vivace_server_thd,
                                  args=(array_ready, test_rgb_array))

    test_main_thd.start()
    server_thd.start()
