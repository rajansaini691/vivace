"""
Sends pixel map to a raspberry pi via a UDP connection
(Based on https://wiki.python.org/moin/UdpCommunication)
"""
import socket
import pickle


class VSocket:
    def __init__(self):
        self.UDP_IP = "169.231.11.31"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def write(self, pixel_map):
        """
        Sends the pixel map to a raspberry pi, where it is rendered live

        Parameters:
            pixel_map       An array of RGB values corresponding to the lights
                            on the LED strip
                            For example, [(0x00,0x00,0x00),(0xFF,0xFF,0xFF)]
                            will be rendered as (BLACK, WHITE)
        """
        # TODO Add validation
        # TODO Add checksum
        # TODO Add timestamp
        data = pickle.dumps(pixel_map)
        self.sock.sendto(data, (self.UDP_IP, self.UDP_PORT))
